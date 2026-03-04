from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Topico, Resposta, Categoria

def lista_forum(request):
    topicos = Topico.objects.filter(ativa=True).order_by('-data_criacao')
    categorias = Categoria.objects.all()
    return render(request, 'forum/lista.html', {'topicos': topicos, 'categorias': categorias})

def detalhe_topico(request, slug):
    topico = get_object_or_404(Topico, slug=slug)
    respostas = topico.respostas.all().order_by('data_postagem')
    return render(request, 'forum/detalhe.html', {'topico': topico, 'respostas': respostas})

@login_required
def curtir_topico(request, slug):
    topico = get_object_or_404(Topico, slug=slug)
    if request.user in topico.likes.all():
        topico.likes.remove(request.user)
    else:
        topico.likes.add(request.user)
        topico.deslikes.remove(request.user) # Se deu like, remove o deslike
    return redirect('detalhe_topico', slug=slug)