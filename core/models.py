from django.db import models
from django.contrib.auth.models import User

class TimeStampedModel(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        abstract = True

class Notificacao(models.Model):
    TIPOS = (
        ('RESPOSTA', 'Nova Resposta'),
        ('MODERACAO', 'Aviso da Moderação'),
        ('AVALIACAO', 'Nova Avaliação'),
    )

    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    mensagem = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criada_em']
        verbose_name_plural = "Notificações"

    def __str__(self):
        return f"{self.tipo} para {self.destinatario.username}"