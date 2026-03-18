from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from forum.models import Topico
from .models import Notificacao
from library.models import LibraryItem

def home(request):
    return render(request, 'core/index.html')

def pesquisa_geral(request):
    query = request.GET.get('q', '')
    escopo = request.GET.get('escopo', 'geral')
    
    resultados_forum = []
    resultados_library = []
    resultados_usuarios = []
    resultados_recursos = []

    if query:
        if escopo in ['geral', 'forum']:
            resultados_forum = Topico.objects.filter(
                Q(titulo__icontains=query) | Q(conteudo__icontains=query),
                ativa=True
            ).select_related('categoria', 'autor').prefetch_related('likes', 'deslikes').order_by('-data_criacao')
            
        if escopo in ['geral', 'library']:
            resultados_library = LibraryItem.objects.filter(
                Q(titulo__icontains=query) | 
                Q(sinopse__icontains=query) |
                Q(diretor_autor_host__icontains=query),
                status='ATIVO'
            ).select_related('usuario_criador').order_by('-id')

        if escopo in ['geral', 'usuarios']:
            resultados_usuarios = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(profile__slug__icontains=query),
                is_active=True
            ).select_related('profile').order_by('username')
            
        if escopo in ['geral', 'recursos']:
            resultados_recursos = []

    total = len(resultados_forum) + len(resultados_library) + len(resultados_usuarios) + len(resultados_recursos)

    contexto = {
        'query': query,
        'escopo': escopo,
        'resultados_forum': resultados_forum,
        'resultados_library': resultados_library,
        'resultados_usuarios': resultados_usuarios,
        'resultados_recursos': resultados_recursos,
        'total': total
    }
    
    return render(request, 'core/pesquisa.html', contexto)


@login_required
def lista_notificacoes(request):
    notificacoes = Notificacao.objects.filter(destinatario=request.user)
    return render(request, 'core/notificacoes.html', {'notificacoes': notificacoes})

@login_required
def marcar_todas_lidas(request):
    Notificacao.objects.filter(destinatario=request.user, lida=False).update(lida=True)
    return redirect('lista_notificacoes')

@login_required
def marcar_lida_e_ir(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk, destinatario=request.user)   
    notificacao.lida = True
    notificacao.save()   
    if notificacao.link and notificacao.link != "#":
        return redirect(notificacao.link)
    return redirect('lista_notificacoes')

@login_required
def limpar_notificacoes(request):
    Notificacao.objects.filter(destinatario=request.user).delete()
    return redirect('lista_notificacoes')