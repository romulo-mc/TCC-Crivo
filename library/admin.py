from django.contrib import admin
from .models import LibraryItem, Categoria, ItemVote, Review

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo')
    list_filter = ('tipo',)

@admin.register(LibraryItem)
class LibraryItemAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'status', 'ano_lancamento', 'usuario_criador')
    list_filter = ('tipo', 'status', 'tags')
    search_fields = ('titulo', 'criador', 'sinopse')
    fieldsets = (
        ('Identificação', {
            'fields': ('status', 'tipo', 'titulo', 'titulo_original', 'ano_lancamento', 'pais_origem', 'criador', 'usuario_criador')
        }),
        ('Mídia', {
            'fields': ('capa', 'link_acesso')
        }),
        ('Descrição', {
            'fields': ('sinopse',)
        }),
        ('Crivo / Acessibilidade', {
            'fields': ('tags', 'tipo_representacao', 'condicao_retratada', 'descricao_detalhada_tema', 'analise_critica', 'participacao_pcd', 'classificacao_etaria')
        }),
        ('Detalhes Específicos', {
            'fields': ('duracao', 'genero', 'plataforma', 'elenco', 'ator_pcd_personagem_pcd', 'editora', 'isbn', 'tem_audiobook', 'tem_ebook_acessivel', 'artista_pcd')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'nota', 'criado_em')
    list_filter = ('nota',)

admin.site.register(ItemVote)