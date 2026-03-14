from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.text import slugify

def criar_categorias_iniciais(sender, **kwargs):
    from .models import Categoria
    
    categorias_padrao = [
        "Vivências e Relatos",
        "Direitos e Acessibilidade",
        "Saúde e Bem-Estar",
        "Reclamação ou Desabafo",
        "Dúvidas e Orientações",
        "Outro"
    ]
    
    for nome in categorias_padrao:
        slug = slugify(nome)
        Categoria.objects.get_or_create(
            slug=slug,
            defaults={'nome': nome, 'descricao': f"Tópicos sobre {nome.lower()}."}
        )

class ForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forum'

    def ready(self):
        post_migrate.connect(criar_categorias_iniciais, sender=self)