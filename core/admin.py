from django.contrib import admin
from .models import Recurso

@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    # Colunas que aparecem na lista
    list_display = ('titulo', 'tipo', 'autor_diretor', 'ano_lancamento')
    
    # Filtros laterais (muito útil para o TCC!)
    list_filter = ('tipo', 'ano_lancamento')
    
    # Barra de busca (pesquisa por título ou conteúdo da sinopse)
    search_fields = ('titulo', 'sinopse', 'autor_diretor')