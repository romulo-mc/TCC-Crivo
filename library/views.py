from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LibraryItemForm, ReviewForm
from .models import Condicao, Gatilho

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
            return redirect('home')
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