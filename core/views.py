from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.contrib.auth.models import User
from forum.models import Topico, Resposta, Categoria
from library.models import LibraryItem, Review, Condicao, Gatilho, CategoriaCondicao, CategoriaGatilho
from educacao.models import RecursoEducativo
from .models import Notificacao
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils.text import slugify
from django.utils import timezone
from feedbacks.models import BugReport, AvaliacaoPlataforma

def home(request):
    return render(request, 'core/index.html')

def pesquisa_geral(request):
    query = request.GET.get('q', '')
    escopo = request.GET.get('escopo', 'geral')
    
    resultados_forum, resultados_library, resultados_usuarios, resultados_recursos = [], [], [], []

    if query:
        if escopo in ['geral', 'forum']:
            resultados_forum = Topico.objects.filter(
                Q(titulo__icontains=query) | Q(conteudo__icontains=query),
                ativa=True
            ).select_related('categoria', 'autor').prefetch_related('likes', 'deslikes').order_by('-data_criacao')
            
        if escopo in ['geral', 'library']:
            resultados_library = LibraryItem.objects.filter(
                Q(titulo__icontains=query) | Q(sinopse__icontains=query) | Q(diretor_autor_host__icontains=query),
                status='ATIVO'
            ).select_related('usuario_criador').order_by('-id')

        if escopo in ['geral', 'usuarios']:
            resultados_usuarios = User.objects.filter(
                Q(username__icontains=query) | Q(first_name__icontains=query) | Q(profile__slug__icontains=query),
                is_active=True
            ).select_related('profile').order_by('username')
            
        if escopo in ['geral', 'recursos']:
            resultados_recursos = RecursoEducativo.objects.filter(
                Q(titulo__icontains=query) | Q(descricao__icontains=query)
            ).select_related('autor').order_by('-data_publicacao')

    total = len(resultados_forum) + len(resultados_library) + len(resultados_usuarios) + len(resultados_recursos)

    return render(request, 'core/pesquisa.html', {
        'query': query, 'escopo': escopo, 'resultados_forum': resultados_forum,
        'resultados_library': resultados_library, 'resultados_usuarios': resultados_usuarios,
        'resultados_recursos': resultados_recursos, 'total': total
    })

@login_required
def lista_notificacoes(request):
    return render(request, 'core/notificacoes.html', {'notificacoes': Notificacao.objects.filter(destinatario=request.user)})

@login_required
def marcar_todas_lidas(request):
    Notificacao.objects.filter(destinatario=request.user, lida=False).update(lida=True)
    return redirect('lista_notificacoes')

@login_required
def marcar_lida_e_ir(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk, destinatario=request.user)   
    notificacao.lida = True
    notificacao.save()   
    if notificacao.link and notificacao.link != "#": return redirect(notificacao.link)
    return redirect('lista_notificacoes')

@login_required
def limpar_notificacoes(request):
    Notificacao.objects.filter(destinatario=request.user).delete()
    return redirect('lista_notificacoes')


@login_required
def painel_moderacao(request):
    if not request.user.is_staff: raise PermissionDenied("Acesso restrito.")
    
    contexto = {
        'topicos_pendentes': Topico.objects.filter(status='PENDENTE').order_by('-data_criacao'),
        'respostas_pendentes': Resposta.objects.filter(status='PENDENTE').order_by('-data_postagem'),
        'acervo_pendente': LibraryItem.objects.filter(status='PENDENTE').order_by('-criado_em'),
        
        'topicos_ocultos': Topico.objects.filter(status__in=['REJEITADO', 'OCULTO']).order_by('-data_atualizacao'),
        'respostas_ocultas': Resposta.objects.filter(status__in=['REJEITADO', 'OCULTO']).order_by('-data_postagem'),
        'acervo_oculto': LibraryItem.objects.filter(status__in=['REJEITADO', 'OCULTO']).order_by('-criado_em'),
        'reviews_ocultas': Review.objects.filter(status='OCULTO').order_by('-criado_em'),
        
        'usuarios_banidos': User.objects.filter(is_active=False).exclude(profile__isnull=True),
        
        'categorias': Categoria.objects.all().order_by('nome'),
        'categorias_condicao': CategoriaCondicao.objects.all().order_by('nome'),
        'categorias_gatilho': CategoriaGatilho.objects.all().order_by('nome'),
        
        'bugs': BugReport.objects.all().order_by('-data_reporte'),
    }

    contexto['total_pendentes'] = contexto['topicos_pendentes'].count() + contexto['respostas_pendentes'].count() + contexto['acervo_pendente'].count()
    return render(request, 'core/painel_moderacao.html', contexto)

@login_required
def aprovar_item(request, tipo, item_id):
    if not request.user.is_staff: raise PermissionDenied()
        
    if tipo == 'topico': obj = get_object_or_404(Topico, id=item_id); obj.status = 'APROVADO'
    elif tipo == 'resposta': obj = get_object_or_404(Resposta, id=item_id); obj.status = 'APROVADO'
    elif tipo == 'acervo': obj = get_object_or_404(LibraryItem, id=item_id); obj.status = 'ATIVO'
    elif tipo == 'review': obj = get_object_or_404(Review, id=item_id); obj.status = 'APROVADO'
    else: return redirect('painel_moderacao')
        
    obj.save() 
    messages.success(request, f"{tipo.capitalize()} readmitido/aprovado com sucesso!")
    return redirect('painel_moderacao')

@login_required
def rejeitar_item(request, tipo, item_id):
    if not request.user.is_staff: raise PermissionDenied()
        
    if request.method == 'POST':
        motivo = request.POST.get('motivo_rejeicao', 'Violação das regras.')
        try:
            if tipo == 'topico': 
                obj = get_object_or_404(Topico, id=item_id)
                obj.status = 'REJEITADO' if obj.status == 'PENDENTE' else 'OCULTO'
                obj.motivo_rejeicao = motivo
            elif tipo == 'resposta': 
                obj = get_object_or_404(Resposta, id=item_id)
                obj.status = 'REJEITADO' if obj.status == 'PENDENTE' else 'OCULTO'
                obj.motivo_rejeicao = motivo
            elif tipo == 'acervo': 
                obj = get_object_or_404(LibraryItem, id=item_id)
                obj.status = 'REJEITADO' if obj.status == 'PENDENTE' else 'OCULTO'
                obj.motivo_rejeicao = motivo
            elif tipo == 'review': 
                obj = get_object_or_404(Review, id=item_id)
                obj.status = 'OCULTO'
                obj.motivo_moderacao = motivo
            else: return redirect('painel_moderacao')

            obj.save() 
            messages.warning(request, f"{tipo.capitalize()} moderado e removido da plataforma com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro interno ao moderar: {str(e)}")
        
        referer = request.META.get('HTTP_REFERER', '')
        if 'moderacao' in referer: return redirect('painel_moderacao')
        elif tipo == 'topico': return redirect('lista_forum')
        elif tipo == 'acervo': return redirect('lista_library')
        elif tipo == 'resposta': return redirect('detalhe_topico', slug=obj.topico.slug)
        elif tipo == 'review': return redirect('detalhe_item', id=obj.item.id)
            
    return redirect('painel_moderacao')

@login_required
def aprovar_massa(request):
    if not request.user.is_staff or request.method != 'POST': raise PermissionDenied()
    tipo = request.POST.get('tipo')
    item_ids = request.POST.getlist('itens_selecionados')
    if not item_ids: return redirect('painel_moderacao')
        
    if tipo == 'topico': Topico.objects.filter(id__in=item_ids).update(status='APROVADO')
    elif tipo == 'resposta': Resposta.objects.filter(id__in=item_ids).update(status='APROVADO')
    elif tipo == 'acervo': LibraryItem.objects.filter(id__in=item_ids).update(status='ATIVO')
            
    messages.success(request, f"{len(item_ids)} itens aprovados!")
    return redirect('painel_moderacao')

@login_required
def toggle_ban_usuario(request, user_id):
    if not request.user.is_staff: raise PermissionDenied()
    usuario = get_object_or_404(User, id=user_id)
    if usuario == request.user or usuario.is_superuser: return redirect(request.META.get('HTTP_REFERER', 'home'))
        
    if usuario.is_active:
        motivo = request.POST.get('motivo_banimento', 'Violação grave.') if request.method == 'POST' else 'Violação.'
        usuario.is_active = False
        usuario.profile.motivo_banimento = motivo
        usuario.profile.data_banimento = timezone.now()
        usuario.profile.save()
        usuario.save()
        messages.warning(request, f"O usuário @{usuario.profile.slug} foi BANIDO.")
    else:
        usuario.is_active = True
        usuario.profile.motivo_banimento = ""
        usuario.profile.data_banimento = None
        usuario.profile.save()
        usuario.save()
        messages.success(request, f"O usuário @{usuario.profile.slug} foi DESBANIDO.")
    return redirect(request.META.get('HTTP_REFERER', 'painel_moderacao'))

@login_required
def adicionar_tag_moderacao(request):
    if not request.user.is_staff or request.method != 'POST': raise PermissionDenied()
    tipo = request.POST.get('tipo_tag')
    nome = request.POST.get('nome')
    
    try:
        if tipo == 'categoria': 
            Categoria.objects.create(nome=nome, slug=slugify(nome))
        elif tipo == 'categoria_condicao':
            CategoriaCondicao.objects.create(nome=nome)
        elif tipo == 'categoria_gatilho':
            CategoriaGatilho.objects.create(nome=nome)
        elif tipo == 'condicao':
            cat_id = request.POST.get('categoria_id')
            cat_obj = CategoriaCondicao.objects.get(id=cat_id) if cat_id else None
            Condicao.objects.create(nome=nome, categoria=cat_obj)
        elif tipo == 'gatilho':
            cat_id = request.POST.get('categoria_id')
            cat_obj = CategoriaGatilho.objects.get(id=cat_id) if cat_id else None
            Gatilho.objects.create(nome=nome, categoria=cat_obj)
            
        messages.success(request, f"Nova tag '{nome}' adicionada!")
    except Exception as e:
        messages.error(request, "Erro: Essa tag já existe ou o nome é inválido.")
        
    return redirect('painel_moderacao')

@login_required
def editar_tag_moderacao(request):
    if not request.user.is_staff or request.method != 'POST': raise PermissionDenied()
    tipo = request.POST.get('tipo_tag')
    tag_id = request.POST.get('tag_id')
    novo_nome = request.POST.get('novo_nome')

    try:
        if tipo == 'categoria':
            obj = get_object_or_404(Categoria, id=tag_id)
            obj.nome = novo_nome; obj.slug = slugify(novo_nome)
        elif tipo == 'categoria_condicao': obj = get_object_or_404(CategoriaCondicao, id=tag_id); obj.nome = novo_nome
        elif tipo == 'categoria_gatilho': obj = get_object_or_404(CategoriaGatilho, id=tag_id); obj.nome = novo_nome
        elif tipo == 'condicao': obj = get_object_or_404(Condicao, id=tag_id); obj.nome = novo_nome
        elif tipo == 'gatilho': obj = get_object_or_404(Gatilho, id=tag_id); obj.nome = novo_nome
        
        obj.save()
        messages.success(request, f"Tag atualizada para '{novo_nome}'!")
    except Exception:
        messages.error(request, "Erro ao atualizar. Verifique se o nome já não existe.")

    return redirect('painel_moderacao')

@login_required
def excluir_tag_moderacao(request, tipo, tag_id):
    if not request.user.is_staff: raise PermissionDenied()
    
    try:
        if tipo == 'categoria': get_object_or_404(Categoria, id=tag_id).delete()
        elif tipo == 'categoria_condicao': get_object_or_404(CategoriaCondicao, id=tag_id).delete()
        elif tipo == 'categoria_gatilho': get_object_or_404(CategoriaGatilho, id=tag_id).delete()
        elif tipo == 'condicao': get_object_or_404(Condicao, id=tag_id).delete()
        elif tipo == 'gatilho': get_object_or_404(Gatilho, id=tag_id).delete()
        messages.success(request, "Item excluído permanentemente!")
    except Exception:
        messages.error(request, "Erro ao excluir o item.")
        
    return redirect('painel_moderacao')