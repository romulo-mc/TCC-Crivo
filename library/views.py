from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import LibraryItemForm, ReviewForm
from .models import Condicao, Gatilho, LibraryItem, Review
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
    review_usuario = reviews.filter(user=request.user).first() if request.user.is_authenticated else None
    ja_avaliou = review_usuario is not None
    
    if request.method == 'POST':
        if ja_avaliou:
            messages.warning(request, 'Você já avaliou esta obra. Use o botão de editar!')
            return redirect('detalhe_item', id=item.id)
            
        form = ReviewForm(request.POST)
        if form.is_valid():
            nova_review = form.save(commit=False)
            nova_review.user = request.user
            nova_review.item = item
            nova_review.save()
            
            messages.success(request, 'Sua avaliação foi registrada com sucesso!')
            return redirect('detalhe_item', id=item.id)
    else:
        form = ReviewForm()
        
    contexto = {
        'item': item,
        'reviews': reviews,
        'review_usuario': review_usuario,
        'total_avaliacoes': reviews.count(),
        'ja_avaliou': ja_avaliou,
        'form': form,
    }
    
    return render(request, 'library/detalhe.html', contexto)

@login_required
def editar_item(request, id):
    item = get_object_or_404(LibraryItem, id=id)
    
    if item.usuario_criador != request.user and not request.user.is_superuser:
        raise PermissionDenied
        
    if request.method == 'POST':
        item_form = LibraryItemForm(request.POST, request.FILES, instance=item)
        if item_form.is_valid():
            item_salvo = item_form.save(commit=False)
            item_salvo.editado = True
            item_salvo.save()
            item_form.save_m2m()
            messages.success(request, 'Obra atualizada com sucesso!')
            return redirect('detalhe_item', id=item.id)
    else:
        item_form = LibraryItemForm(instance=item)

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
        'editando': True,
        'condicoes_dict': condicoes_dict,
        'gatilhos_dict': gatilhos_dict,
        'item': item
    })

@login_required
def editar_review(request, id):
    review = get_object_or_404(Review, id=id)
    
    if review.user != request.user and not request.user.is_superuser:
        raise PermissionDenied
        
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review_salva = form.save(commit=False)
            review_salva.editado = True
            review_salva.save()
            messages.success(request, 'Sua avaliação foi atualizada!')
            return redirect('detalhe_item', id=review.item.id)
    else:
        form = ReviewForm(instance=review)
        
    return render(request, 'library/editar_review.html', {'form': form, 'review': review})