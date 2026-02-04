from django.shortcuts import render
from rest_framework import viewsets
from .models import Recurso
from .serializers import RecursoSerializer


class RecursoViewSet(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer
    
def index(request):
    recursos = Recurso.objects.all()
    print ("Quantos filmes achei: ",recursos.count())
    print("Primeiro filme: ",recursos.first())
    context = {
        'recursos': recursos
    }
    return render(request, 'index.html', context)