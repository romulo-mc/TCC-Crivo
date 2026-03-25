from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AvaliacaoPlataforma
from .forms import BugReportForm, AvaliacaoPlataformaForm

def reportar_bug(request):
    if request.method == 'POST':
        form = BugReportForm(request.POST, request.FILES)
        if form.is_valid():
            bug = form.save(commit=False)
            if request.user.is_authenticated:
                bug.usuario = request.user
            bug.save()
            messages.success(request, "Bug reportado com sucesso! Nossa equipe já vai dar uma olhada. 🐛🔨")
        else:
            messages.error(request, "Erro ao enviar o reporte. Tente novamente.")
            
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def avaliar_plataforma(request):
    avaliacao_existente = AvaliacaoPlataforma.objects.filter(usuario=request.user).first()
    
    if request.method == 'POST':
        form = AvaliacaoPlataformaForm(request.POST, instance=avaliacao_existente)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.usuario = request.user
            avaliacao.save()
            messages.success(request, "Avaliação salva com sucesso! Muito obrigada por ajudar a melhorar o Crivo! 🌟")
            return redirect('perfil_usuario', slug=request.user.profile.slug)
    else:
        form = AvaliacaoPlataformaForm(instance=avaliacao_existente)
        
    return render(request, 'feedbacks/avaliar.html', {
        'form': form, 
        'ja_avaliou': bool(avaliacao_existente)
    })