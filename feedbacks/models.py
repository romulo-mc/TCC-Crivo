from django.db import models
from django.contrib.auth.models import User

class BugReport(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ANALISE', 'Em Análise'),
        ('RESOLVIDO', 'Resolvido'),
        ('DESCARTADO', 'Descartado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bugs_reportados')
    
    url_erro = models.URLField(max_length=500, blank=True, verbose_name="Onde o erro aconteceu?")
    descricao = models.TextField(verbose_name="Descrição do Bug")
    print_tela = models.ImageField(upload_to='bugs/', blank=True, null=True, verbose_name="Print da Tela (Opcional)")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    data_reporte = models.DateTimeField(auto_now_add=True)
    resolucao = models.TextField(blank=True, verbose_name="Nota de Resolução (Para o Admin anotar o que fez)")

    def __str__(self):
        return f"Bug #{self.id} - {self.get_status_display()}"

    class Meta:
        verbose_name = "Reporte de Bug"
        verbose_name_plural = "Reportes de Bugs"
        ordering = ['-data_reporte']


class AvaliacaoPlataforma(models.Model):
    NOTA_CHOICES = [(i, str(i)) for i in range(1, 6)] # Estrelas de 1 a 5

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avaliacao_plataforma')
    
    nota_geral = models.IntegerField(choices=NOTA_CHOICES, verbose_name="Nota Geral para a Plataforma")
    nota_usabilidade = models.IntegerField(choices=NOTA_CHOICES, verbose_name="Facilidade de Uso (Usabilidade)")
    nota_acessibilidade = models.IntegerField(choices=NOTA_CHOICES, verbose_name="Acessibilidade e Inclusão")
    nota_design = models.IntegerField(choices=NOTA_CHOICES, verbose_name="Design e Visual")
    
    probabilidade_recomendar = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, 11)],
        verbose_name="Qual a probabilidade de você recomendar o Crivo para um amigo? (0 a 10)"
    )
    
    feedback_aberto = models.TextField(blank=True, verbose_name="Sugestões, críticas ou elogios (Opcional)")
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.usuario.username} - Nota: {self.nota_geral}"

    class Meta:
        verbose_name = "Avaliação da Plataforma"
        verbose_name_plural = "Avaliações da Plataforma"
        ordering = ['-data_avaliacao']