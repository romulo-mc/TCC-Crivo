from django.db import models
from django.contrib.auth.models import User

class RecursoEducativo(models.Model):
    TIPO_CHOICES = [
        ('IMAGEM', 'Imagem / Infográfico'),
        ('VIDEO', 'Vídeo (Upload Local)'),
        ('AUDIO', 'Áudio (Upload Local)'),
        ('PDF', 'Documento (PDF)'),
        ('EMBED', 'Vídeo/Podcast (YouTube/Spotify)'),
        ('LINK', 'Link Externo (Artigos/Sites)'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título do Recurso")
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='IMAGEM')
    descricao = models.TextField(verbose_name="Descrição / Legenda")
    
    arquivo = models.FileField(upload_to='educacao/arquivos/', blank=True, null=True, help_text="Upload do arquivo (PDF, MP3, MP4, JPG, PNG).")
    capa = models.ImageField(upload_to='educacao/capas/', blank=True, null=True, help_text="Capa ilustrativa (ideal para Links, Áudios ou PDFs).")
    
    alt_text = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Texto Alternativo da Imagem (Acessibilidade)",
        help_text="Descreva a imagem/capa para pessoas com deficiência visual (leitores de tela)."
    )
    
    codigo_incorporacao = models.TextField(
        blank=True, null=True, 
        verbose_name="Código de Incorporação (Iframe)",
        help_text="Cole o código '<iframe...>' do YouTube ou Spotify."
    )
    url_externa = models.URLField(blank=True, null=True, verbose_name="URL Externa")
    
    baixar_pdf = models.BooleanField(
        default=False, 
        verbose_name="Forçar download do PDF?",
        help_text="Marque para o botão fazer o download. Desmarque para abrir em nova aba."
    )
    
    autor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    data_publicacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Recurso Educativo'
        verbose_name_plural = 'Recursos Educativos'
        ordering = ['-data_publicacao']

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.titulo}"

    @property
    def get_media_type(self):
        if self.tipo in ['IMAGEM', 'VIDEO', 'PDF'] and self.arquivo: return 'ARQUIVO'
        if self.tipo == 'AUDIO' and self.arquivo: return 'AUDIO'
        if self.tipo == 'EMBED' and self.codigo_incorporacao: return 'EMBED'
        if self.tipo == 'LINK' and self.capa: return 'LINK_CAPA'
        return None