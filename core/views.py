from django.shortcuts import render
from library.models import LibraryItem
from django.db.models import Q
from forum.models import Topico
from library.models import LibraryItem

def home(request):
    return render(request, 'core/index.html')

def pesquisa_geral(request):
    query = request.GET.get('q', '')
    escopo = request.GET.get('escopo', 'geral')
    
    resultados_forum = []
    resultados_library = []

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

    contexto = {
        'query': query,
        'escopo': escopo,
        'resultados_forum': resultados_forum,
        'resultados_library': resultados_library,
        'total': len(resultados_forum) + len(resultados_library)
    }
    
    return render(request, 'core/pesquisa.html', contexto)