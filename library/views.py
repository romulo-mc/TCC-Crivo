from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LibraryItemForm, ReviewForm
from .models import Condicao, Gatilho, LibraryItem
from django.db.models import Avg


@login_required
def lista_library(request):
    request.session['ultimo_contexto'] = 'library'
    
    itens = LibraryItem.objects.filter(status='ATIVO').prefetch_related('condicoes', 'gatilhos', 'reviews').order_by('-id')
    
    tipos_selecionados = request.GET.getlist('tipo')
    if tipos_selecionados:
        itens = itens.filter(tipo__in=tipos_selecionados)
        
    condicoes_selecionadas = request.GET.getlist('condicoes')
    if condicoes_selecionadas:
        itens = itens.filter(condicoes__id__in=condicoes_selecionadas).distinct()

    gatilhos_selecionados = request.GET.getlist('gatilhos')
    if gatilhos_selecionados:
        itens = itens.filter(gatilhos__id__in=gatilhos_selecionados).distinct()

    condicoes_dict = {}
    for c in Condicao.objects.all().order_by('categoria', 'nome'):
        cat = c.get_categoria_display() or "Outros"
        if cat not in condicoes_dict: condicoes_dict[cat] = []
        condicoes_dict[cat].append(c)

    gatilhos_dict = {}
    for g in Gatilho.objects.all().order_by('categoria', 'nome'):
        cat = g.get_categoria_display() or "Outros"
        if cat not in gatilhos_dict: gatilhos_dict[cat] = []
        gatilhos_dict[cat].append(g)

    contexto = {
        'itens': itens,
        'tipos_disponiveis': LibraryItem.TIPO_CHOICES,
        'condicoes_dict': condicoes_dict,
        'gatilhos_dict': gatilhos_dict,
        'tipos_selecionados': tipos_selecionados,
        'condicoes_selecionadas': [int(i) for i in condicoes_selecionadas if i.isdigit()],
        'gatilhos_selecionados': [int(i) for i in gatilhos_selecionados if i.isdigit()],
    }
    
    return render(request, 'library/lista.html', contexto)

@login_required
def adicionar_item(request):
    if request.method == 'POST':
        item_form = LibraryItemForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if item_form.is_valid() and review_form.is_valid():
            item = item_form.save(commit=False)
            item.usuario_criador = request.user
            item.save()
            item_form.save_m2m() 

            review = review_form.save(commit=False)
            review.user = request.user
            review.item = item
            review.save()

            messages.success(request, 'Item enviado com sucesso! Aguardando moderação.')
            return redirect('lista_library')
        else:
            messages.error(request, 'Houve um erro no formulário. Verifique os campos.')
            
    else:
        item_form = LibraryItemForm()
        review_form = ReviewForm()

    condicoes_dict = {}
    for c in Condicao.objects.all().order_by('categoria', 'nome'):
        cat = c.get_categoria_display() or "Outros"
        if cat not in condicoes_dict: condicoes_dict[cat] = []
        condicoes_dict[cat].append(c)

    gatilhos_dict = {}
    for g in Gatilho.objects.all().order_by('categoria', 'nome'):
        cat = g.get_categoria_display() or "Outros"
        if cat not in gatilhos_dict: gatilhos_dict[cat] = []
        gatilhos_dict[cat].append(g)

    return render(request, 'library/adicionar_item.html', {
        'item_form': item_form,
        'review_form': review_form,
        'condicoes_dict': condicoes_dict,
        'gatilhos_dict': gatilhos_dict,
    })
    

@login_required
def detalhe_item(request, id):
    request.session['ultimo_contexto'] = 'library'
    item = get_object_or_404(LibraryItem, id=id, status='ATIVO')
    reviews = item.reviews.all().order_by('-criado_em')
    review_autor = reviews.filter(user=item.usuario_criador).first()
    ja_avaliou = reviews.filter(user=request.user).exists()
    
    if request.method == 'POST':
        if ja_avaliou:
            messages.warning(request, 'Você já avaliou esta obra.')
            return redirect('detalhe_item', id=item.id)
            
        form = ReviewForm(request.POST)
        if form.is_valid():
            nova_review = form.save(commit=False)
            nova_review.user = request.user
            nova_review.item = item
            nova_review.comentario_justificativa = "" 
            nova_review.save()
            
            messages.success(request, 'Sua avaliação foi registrada com sucesso!')
            return redirect('detalhe_item', id=item.id)
    else:
        form = ReviewForm()
        
    contexto = {
        'item': item,
        'review_autor': review_autor,
        'total_avaliacoes': reviews.count(),
        'ja_avaliou': ja_avaliou,
        'form': form,
    }
    
    return render(request, 'library/detalhe.html', contexto)