from rest_framework import viewsets
from .models import Recurso
from .serializers import RecursoSerializer

class RecursoViewSet(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer