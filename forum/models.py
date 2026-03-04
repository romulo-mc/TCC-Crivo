from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def __cl__str__(self):
        return self.nome

class Topico(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='topicos')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativa = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='topico_likes', blank=True)
    deslikes = models.ManyToManyField(User, related_name='topico_deslikes', blank=True)

    def __str__(self):
        return self.titulo
    
    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_deslikes(self):
        return self.deslikes.count()

class Resposta(models.Model):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='respostas')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_postagem = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='resposta_likes', blank=True)
    deslikes = models.ManyToManyField(User, related_name='resposta_deslikes', blank=True)
    
    def __str__(self):
        return f"Resposta de {self.autor.username} em {self.topico.titulo}"