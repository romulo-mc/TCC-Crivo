from django.contrib import admin
from .models import Categoria, Topico, Resposta

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}

@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'autor', 'data_criacao')
    prepopulated_fields = {'slug': ('titulo',)}

admin.site.register(Resposta)