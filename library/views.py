from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LibraryItemForm

@login_required
def adicionar_item(request):
    if request.method == 'POST':
        form = LibraryItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.usuario_criador = request.user
            item.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = LibraryItemForm()
    
    return render(request, 'library/adicionar_item.html', {'form': form})