from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import RecursoEducativo
from .forms import RecursoEducativoForm

def lista_recursos(request):
    request.session['ultimo_contexto'] = 'educacao'
    posts = RecursoEducativo.objects.all()
    return render(request, 'educacao/lista.html', {'posts': posts})

@login_required
def criar_recurso(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = RecursoEducativoForm(request.POST, request.FILES)
        if form.is_valid():
            recurso = form.save(commit=False)
            recurso.autor = request.user
            recurso.save()
            return redirect('lista_recursos')
    else:
        form = RecursoEducativoForm()
    return render(request, 'educacao/form_recurso.html', {'form': form, 'editando': False})

@login_required
def editar_recurso(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    recurso = get_object_or_404(RecursoEducativo, pk=pk)
    if request.method == 'POST':
        form = RecursoEducativoForm(request.POST, request.FILES, instance=recurso)
        if form.is_valid():
            form.save()
            return redirect('lista_recursos')
    else:
        form = RecursoEducativoForm(instance=recurso)
    return render(request, 'educacao/form_recurso.html', {'form': form, 'editando': True, 'recurso': recurso})

@login_required
def deletar_recurso(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    recurso = get_object_or_404(RecursoEducativo, pk=pk)
    if request.method == 'POST':
        recurso.delete()
        return redirect('lista_recursos')
    return render(request, 'educacao/confirmar_delete.html', {'recurso': recurso})