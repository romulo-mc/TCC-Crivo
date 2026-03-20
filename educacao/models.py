from django.db import models
from django.contrib.auth.models import User

class RecursoEducativo(models.Model):
    TIPO_CHOICES = [
        ('IMAGEM', 'Imagem / Infográfico'),
        ('VIDEO', 'Vídeo (Upload)'),
        ('AUDIO', 'Áudio / Podcast (Upload)'),
        ('PDF', 'Documento (PDF)'),
        ('EMBED', 'Vídeo/Podcast (YouTube/Spotify)'),
        ('LINK', 'Link Externo (Artigos/Sites)'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título do Recurso")
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='IMAGEM')
    
    descricao = models.TextField(verbose_name="Descrição / Legenda") 
    arquivo = models.FileField(upload_to='educacao/arquivos/', blank=True, null=True, help_text="Faça o upload do arquivo aqui se não for Link ou Embed.")
    capa = models.ImageField(upload_to='educacao/capas/', blank=True, null=True, help_text="Capa ilustrativa (ideal para links externos e áudios).")
    codigo_incorporacao = models.TextField(
        blank=True, null=True, 
        verbose_name="Código de Incorporação (Iframe)",
        help_text="Cole aqui o código <iframe...> fornecido pelo YouTube, Spotify, etc."
    )
    
    url_externa = models.URLField(blank=True, null=True, verbose_name="Link Externo", help_text="Obrigatório se o tipo for 'Link Externo'.")
    
    autor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    data_publicacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Recurso Educativo'
        verbose_name_plural = 'Recursos Educativos'
        ordering = ['-data_publicacao']

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.titulo}"