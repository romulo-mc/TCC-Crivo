from django.contrib import admin
from .models import Recurso

@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'autor_diretor', 'ano_lancamento')
    
    list_filter = ('tipo', 'ano_lancamento')
    
    search_fields = ('titulo', 'sinopse', 'autor_diretor')