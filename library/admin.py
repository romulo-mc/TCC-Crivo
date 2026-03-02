from django.contrib import admin
from .models import Condicao, Gatilho, LibraryItem, Review

# Registrando as novas categorias separadas
admin.site.register(Condicao)
admin.site.register(Gatilho)
admin.site.register(Review)

@admin.register(LibraryItem)
class LibraryItemAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'status', 'usuario_criador', 'criado_em')
    list_filter = ('status', 'tipo')
    search_fields = ('titulo', 'diretor_autor_host')
    actions = ['aprovar_itens']

    # Uma ação rápida para você aprovar vários itens de uma vez só!
    def aprovar_itens(self, request, queryset):
        queryset.update(status='ATIVO')
    aprovar_itens.short_description = "Aprovar itens selecionados"