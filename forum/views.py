from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from django.core.exceptions import PermissionDenied
from .models import Topico, Resposta, Categoria
from .forms import TopicoForm, RespostaForm
import uuid
from django.http import JsonResponse
from django.db.models import Count, Sum

@login_required
def lista_forum(request):
    request.session['ultimo_contexto'] = 'forum'
    topicos = Topico.objects.filter(ativa=True, status='APROVADO')
    filtro = request.GET.get('ordem')
    categoria_slug = request.GET.get('categoria')
    if categoria_slug:
        topicos = topicos.filter(categoria__slug=categoria_slug)

    if filtro == 'novos':
        topicos = topicos.order_by('-data_criacao')
    elif filtro == 'antigos':
        topicos = topicos.order_by('data_criacao')
    elif filtro == 'populares':
        topicos = topicos.annotate(num_respostas=Count('respostas')).order_by('-num_respostas')
    elif filtro == 'votos':
        topicos = topicos.annotate(
            score=Count('likes') - Count('deslikes')
        ).order_by('-score')
    else:
        topicos = topicos.order_by('-data_criacao')

    categorias = Categoria.objects.all()

    categoria_atual_nome = None
    if categoria_slug:
        cat_obj = Categoria.objects.filter(slug=categoria_slug).first()
        if cat_obj:
            categoria_atual_nome = cat_obj.nome

    return render(request, 'forum/lista.html', {
        'topicos': topicos,
        'categorias': categorias,
        'categoria_atual_nome': categoria_atual_nome,
    })

@login_required
def detalhe_topico(request, slug):
    request.session['ultimo_contexto'] = 'forum'
    topico = get_object_or_404(Topico, slug=slug, ativa=True)

    if topico.status != 'APROVADO' and request.user != topico.autor and not request.user.is_staff:
        raise PermissionDenied("Este tópico ainda não foi aprovado pela moderação.")

    if request.user.is_staff:
        respostas = topico.respostas.filter(pai__isnull=True).order_by('data_postagem')
    else:
        respostas = topico.respostas.filter(pai__isnull=True, status='APROVADO').order_by('data_postagem')

    if request.method == 'POST':
        form = RespostaForm(request.POST)
        if form.is_valid():
            resposta = form.save(commit=False)
            resposta.autor = request.user
            resposta.topico = topico

            pai_id = request.POST.get('pai_id')
            if pai_id:
                pai = get_object_or_404(Resposta, id=pai_id)
                resposta.pai = pai

            resposta.save()
            messages.success(request, 'Resposta enviada com sucesso!')
            return redirect('detalhe_topico', slug=topico.slug)
    else:
        form = RespostaForm()

    return render(request, 'forum/detalhe_topico.html', {
        'topico': topico,
        'respostas': respostas,
        'form': form
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

@login_required
def editar_topico(request, slug):
    topico = get_object_or_404(Topico, slug=slug)
    if topico.autor != request.user and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        form = TopicoForm(request.POST, instance=topico)
        if form.is_valid():
            topico_salvo = form.save(commit=False)
            if not topico.editado:
                topico_banco = Topico.objects.get(pk=topico.pk)
                topico_salvo.conteudo_original = topico_banco.conteudo
                topico_salvo.editado = True

            topico_salvo.save()
            return redirect('detalhe_topico', slug=topico.slug)
    else:
        form = TopicoForm(instance=topico)

    return render(request, 'forum/criar_topico.html', {'form': form, 'editando': True, 'topico': topico})

@login_required
def editar_resposta(request, id):
    resposta = get_object_or_404(Resposta, id=id)

    if resposta.autor != request.user and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        novo_conteudo = request.POST.get('conteudo')
        if novo_conteudo:
            if not resposta.editado:
                resposta_banco = Resposta.objects.get(pk=resposta.pk)
                resposta.conteudo_original = resposta_banco.conteudo
                resposta.editado = True

            resposta.conteudo = novo_conteudo
            resposta.save()
            return redirect('detalhe_topico', slug=resposta.topico.slug)

    return render(request, 'forum/editar_resposta.html', {'resposta': resposta})