from django.contrib import admin
from .models import RecursoEducativo

@admin.register(RecursoEducativo)
class RecursoEducativoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'autor', 'data_publicacao')
    list_filter = ('tipo', 'data_publicacao', 'autor')
    search_fields = ('titulo', 'descricao')
    date_hierarchy = 'data_publicacao'