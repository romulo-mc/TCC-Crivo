from django.shortcuts import render
from library.models import LibraryItem 

def home(request):
    itens = LibraryItem.objects.filter(status='ATIVO').order_by('-criado_em')[:6]

    return render(request, 'core/index.html', {'itens': itens})