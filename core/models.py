from django.db import models

class Recurso(models.Model):
    # Opções para o campo 'tipo'
    TIPO_CHOICES = [
        ('FILME', 'Filme'),
        ('SERIE', 'Série'),
        ('LIVRO', 'Livro'),
        ('ARTIGO', 'Artigo Acadêmico'),
        ('PODCAST', 'Podcast'),
    ]

    # Campos Básicos
    titulo = models.CharField("Título", max_length=200)
    tipo = models.CharField("Tipo de Mídia", max_length=20, choices=TIPO_CHOICES)
    
    # Detalhes
    sinopse = models.TextField("Sinopse / Descrição", blank=True, null=True)
    autor_diretor = models.CharField("Autor ou Diretor", max_length=150, blank=True, null=True)
    ano_lancamento = models.PositiveIntegerField("Ano de Lançamento", blank=True, null=True)
    
    # Conteúdo
    link_acesso = models.URLField("Link para acessar (Netflix, PDF, YouTube)", blank=True, null=True)
    
    # Imagem
    url_capa = models.URLField("URL da Imagem de Capa", blank=True, null=True)

    # Auditoria
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos do Acervo"
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"