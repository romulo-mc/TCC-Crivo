from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Topico, Resposta, Categoria
from .forms import TopicoForm
import uuid
from django.http import JsonResponse

def lista_forum(request):
    request.session['ultimo_contexto'] = 'forum'
    topicos = Topico.objects.filter(ativa=True, status='APROVADO').order_by('-data_criacao')
    categorias = Categoria.objects.all()
    return render(request, 'forum/lista.html', {'topicos': topicos, 'categorias': categorias})

@login_required
def detalhe_topico(request, slug):
    topico = get_object_or_404(Topico, slug=slug, status='APROVADO')
    respostas_raiz = topico.respostas.filter(pai__isnull=True, status='APROVADO').order_by('-data_postagem')
    
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        pai_id = request.POST.get('pai_id')
        
        if conteudo:
            pai_obj = Resposta.objects.get(id=pai_id) if pai_id else None
            Resposta.objects.create(
                topico=topico,
                autor=request.user,
                conteudo=conteudo,
                pai=pai_obj
            )
            return redirect('detalhe_topico', slug=slug)

    return render(request, 'forum/detalhe_topico.html', {
        'topico': topico,
        'respostas': respostas_raiz
    })
    
@login_required
def criar_topico(request):
    if request.method == 'POST':
        form = TopicoForm(request.POST)
        if form.is_valid():
            topico = form.save(commit=False)
            topico.autor = request.user
            novo_slug = slugify(topico.titulo)
            if Topico.objects.filter(slug=novo_slug).exists():
                novo_slug = f"{novo_slug}-{str(uuid.uuid4())[:8]}"
            topico.slug = novo_slug
            topico.save()
            return redirect('detalhe_topico', slug=topico.slug)
    else:
        form = TopicoForm()
    
    return render(request, 'forum/criar_topico.html', {'form': form})

@login_required
def votar_topico(request, slug, tipo):
    topico = get_object_or_404(Topico, slug=slug)
    if tipo == 'like':
        if request.user in topico.likes.all():
            topico.likes.remove(request.user)
        else:
            topico.likes.add(request.user)
            topico.deslikes.remove(request.user)
    else:
        if request.user in topico.deslikes.all():
            topico.deslikes.remove(request.user)
        else:
            topico.deslikes.add(request.user)
            topico.likes.remove(request.user)
            
    user_voto = 'nenhum'
    if request.user in topico.likes.all():
        user_voto = 'like'
    elif request.user in topico.deslikes.all():
        user_voto = 'deslike'
    
    return JsonResponse({'total': topico.total_votos, 'user_voto': user_voto})

@login_required
def votar_resposta(request, id, tipo):
    resposta = get_object_or_404(Resposta, id=id)
    if tipo == 'like':
        if request.user in resposta.likes.all():
            resposta.likes.remove(request.user)
        else:
            resposta.likes.add(request.user)
            resposta.deslikes.remove(request.user)
    else:
        if request.user in resposta.deslikes.all():
            resposta.deslikes.remove(request.user)
        else:
            resposta.deslikes.add(request.user)
            resposta.likes.remove(request.user)
            
    user_voto = 'nenhum'
    if request.user in resposta.likes.all():
        user_voto = 'like'
    elif request.user in resposta.deslikes.all():
        user_voto = 'deslike'
            
    return JsonResponse({'total': resposta.total_votos, 'user_voto': user_voto})