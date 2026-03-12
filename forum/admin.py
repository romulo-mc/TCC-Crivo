from django.contrib import admin
from .models import Categoria, Topico, Resposta

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}

@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'autor', 'status', 'data_criacao')
    list_filter = ('status', 'categoria', 'data_criacao')
    search_fields = ('titulo', 'autor__username', 'conteudo')
    list_editable = ('status',) 
    prepopulated_fields = {'slug': ('titulo',)}

@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ('id', 'topico', 'autor', 'status', 'data_postagem')
    list_filter = ('status', 'data_postagem')
    search_fields = ('conteudo', 'autor__username')
    list_editable = ('status',)