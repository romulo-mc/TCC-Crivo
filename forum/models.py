from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nome

class Topico(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
        ('OCULTO', 'Ocultado pela Moderação') 
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APROVADO')
    
    motivo_rejeicao = models.TextField(blank=True, verbose_name="Motivo da Rejeição/Ocultação (Admin)")
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='topicos')
    outra_categoria = models.CharField(max_length=100, blank=True, null=True, help_text="Se selecionou 'Outro', especifique aqui.")
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='topicos')
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativa = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='topico_likes', blank=True)
    deslikes = models.ManyToManyField(User, related_name='topico_deslikes', blank=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    editado = models.BooleanField(default=False)
    conteudo_original = models.TextField(blank=True, null=True, help_text="Visível apenas para admins")

    def __str__(self):
        return self.titulo
    
    @property
    def total_votos(self):
        return self.likes.count() - self.deslikes.count()

class Resposta(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
        ('OCULTO', 'Ocultado pela Moderação')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APROVADO')
    motivo_rejeicao = models.TextField(blank=True, verbose_name="Motivo da Rejeição/Ocultação (Admin)")
    
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='respostas')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_postagem = models.DateTimeField(auto_now_add=True)
    pai = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='filhas')
    likes = models.ManyToManyField(User, related_name='resposta_likes', blank=True)
    deslikes = models.ManyToManyField(User, related_name='resposta_deslikes', blank=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    editado = models.BooleanField(default=False)
    conteudo_original = models.TextField(blank=True, null=True, help_text="Visível apenas para admins")
    def __str__(self):
        if self.pai:
            return f"Réplica de {self.autor.username} ao comentário {self.pai.id}"
        return f"Comentário de {self.autor.username} no tópico {self.topico.titulo}"

    @property
    def total_votos(self):
        return self.likes.count() - self.deslikes.count()