from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel

class CategoriaCondicao(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nome

class CategoriaGatilho(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nome

class Condicao(models.Model):
    TIPO_CHOICES = [
        ('FISICA', 'Física'), ('SENSORIAL', 'Sensorial'), 
        ('INTELECTUAL', 'Intelectual'), ('PSICOSSOCIAL', 'Psicossocial'), 
        ('MULTIPLA', 'Múltipla'), ('OUTRO', 'Outro')
    ]
    nome = models.CharField(max_length=100, unique=True)
    categoria = models.ForeignKey(CategoriaCondicao, on_delete=models.CASCADE, related_name='condicoes', null=True, blank=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, blank=True)

    def __str__(self): return self.nome

class Gatilho(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    categoria = models.ForeignKey(CategoriaGatilho, on_delete=models.CASCADE, related_name='gatilhos', null=True, blank=True)

    def __str__(self): return self.nome

class LibraryItem(TimeStampedModel):
    STATUS_CHOICES = [('PENDENTE', 'Pendente'), ('ATIVO', 'Aprovado'), ('REJEITADO', 'Rejeitado'), ('OCULTO', 'Ocultado (Moderação)')]
    TIPO_CHOICES = [('FILME', 'Filme'), ('SERIE', 'Série'), ('LIVRO', 'Livro'), ('MUSICA', 'Música'), ('PODCAST', 'Podcast'), ('ARTIGO', 'Artigo')]
    TIPO_REP_CHOICES = [
        ('PROTAGONISMO', 'Protagonismo'), ('COADJUVANTE', 'Coadjuvante com Arco Próprio'),
        ('MULETA', 'Personagem "Muleta" (Token)'), ('ALIVIO', 'Alívio Cômico'),
        ('VILAO', 'Vilão Estereotipado'), ('OUTRO', 'Outro (Especificar)')
    ]
    ABORDAGEM_CHOICES = [
        ('SOCIAL', 'Modelo Social'), ('MEDICO', 'Modelo Médico / Tragédia'),
        ('INSPIRACIONAL', 'Pornografia Inspiracional (Inspiration Porn)'),
        ('ASSISTENCIALISTA', 'Assistencialista / Paternalista'), ('OUTRO', 'Outro (Especificar)')
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    motivo_rejeicao = models.TextField(blank=True, verbose_name="Motivo da Rejeição/Ocultação (Admin)")
    usuario_criador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='itens_cadastrados')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200, verbose_name="Título")
    ano_lancamento = models.PositiveIntegerField(null=True, blank=True)
    pais_origem = models.CharField(max_length=100, blank=True)
    idioma = models.CharField(max_length=50, blank=True)
    classificacao_indicativa = models.CharField(max_length=20, blank=True)
    
    capa = models.ImageField(upload_to='library/covers/', blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="Texto Alternativo da Capa")
    
    link_acesso = models.URLField(blank=True, null=True)
    titulo_original = models.CharField(max_length=200, blank=True)
    sinopse = models.TextField(blank=True)
    duracao = models.CharField(max_length=50, blank=True)
    genero = models.CharField(max_length=100, blank=True)
    diretor_autor_host = models.CharField(max_length=200, blank=True, verbose_name="Diretor / Autor / Artista / Host")
    distribuidora_editora = models.CharField(max_length=100, blank=True)
    plataforma = models.CharField(max_length=200, blank=True)
    numero_temporadas_paginas = models.PositiveIntegerField(null=True, blank=True)
    isbn_doi = models.CharField(max_length=100, blank=True)
    album = models.CharField(max_length=200, blank=True)
    elenco_principal = models.TextField(blank=True)
    tem_personagem_pcd = models.BooleanField(default=False)
    ator_pcd_interpreta = models.BooleanField(default=False)
    condicoes = models.ManyToManyField('Condicao', blank=True, related_name='itens')
    gatilhos = models.ManyToManyField('Gatilho', blank=True, related_name='itens')
    condicao_outra = models.CharField(max_length=200, blank=True)
    gatilho_outro = models.CharField(max_length=200, blank=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    editado = models.BooleanField(default=False)
    tipo_representacao = models.CharField(max_length=50, choices=TIPO_REP_CHOICES, blank=True) 
    tipo_representacao_outro = models.CharField(max_length=100, blank=True)
    abordagem = models.CharField(max_length=50, choices=ABORDAGEM_CHOICES, blank=True) 
    abordagem_outro = models.CharField(max_length=100, blank=True)
    descricao_representacao = models.TextField(blank=True)
    analise_critica = models.TextField(blank=True) 
    COMBATE_REFORCA = [('COMBATE', 'Combate o capacitismo'), ('REFORCA', 'Reforça o capacitismo'), ('MISTO', 'Misto'), ('NEUTRO', 'Neutro')]
    combate_ou_reforca = models.CharField(max_length=20, choices=COMBATE_REFORCA, blank=True)
    pontos_positivos = models.TextField(blank=True)
    pontos_problematicos = models.TextField(blank=True)

    def __str__(self): return self.titulo
    
    @property
    def elenco_lista(self):
        if self.elenco_principal:
            return [ator.strip() for ator in self.elenco_principal.split(',') if ator.strip()]
        return []

    @property
    def media_notas(self):
        from django.db.models import Avg
        media = self.reviews.aggregate(Avg('nota_geral'))['nota_geral__avg']
        return round(media, 1) if media else 0
    
class Review(TimeStampedModel):
    STATUS_CHOICES = [('APROVADO', 'Aprovado'), ('OCULTO', 'Ocultado (Moderação)')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APROVADO')
    motivo_moderacao = models.TextField(blank=True, verbose_name="Motivo Ocultação (Admin)")
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(LibraryItem, on_delete=models.CASCADE, related_name='reviews')
    nota_geral = models.PositiveIntegerField(choices=RATING_CHOICES)
    nota_representatividade = models.PositiveIntegerField(choices=RATING_CHOICES)
    nota_critica = models.PositiveIntegerField(choices=RATING_CHOICES)
    comentario_justificativa = models.TextField(blank=True, verbose_name="Justificativa das notas")
    data_atualizacao = models.DateTimeField(auto_now=True)
    editado = models.BooleanField(default=False)    

    class Meta:
        unique_together = ('user', 'item')