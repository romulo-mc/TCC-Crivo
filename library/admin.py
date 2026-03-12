from django.contrib import admin
from .models import Condicao, Gatilho, LibraryItem, Review

admin.site.register(Condicao)
admin.site.register(Gatilho)
admin.site.register(Review)

@admin.register(LibraryItem)
class LibraryItemAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'status', 'usuario_criador', 'criado_em')
    list_filter = ('status', 'tipo')
    search_fields = ('titulo', 'diretor_autor_host')
    list_editable = ('status',) 
    
    actions = ['aprovar_itens', 'rejeitar_itens']

    def aprovar_itens(self, request, queryset):
        queryset.update(status='ATIVO') 
    aprovar_itens.short_description = "Marcar selecionados como Aprovados"

    def rejeitar_itens(self, request, queryset):
        queryset.update(status='REJEITADO')
    rejeitar_itens.short_description = "Marcar selecionados como Rejeitados"