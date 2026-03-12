from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel

class Condicao(models.Model):
    CATEGORIA_CHOICES = [
        ('NEURO', 'Neurodesenvolvimento'),
        ('NEUROLOGICA', 'Condições Neurológicas'),
        ('FISICA', 'Deficiências Físicas / Motoras'),
        ('AUDITIVA', 'Deficiência Auditiva'),
        ('VISUAL', 'Deficiência Visual'),
        ('GENETICA', 'Condições Genéticas / Síndromes'),
        ('CRONICA', 'Condições Crônicas e Invisíveis'),
        ('PSICOSSOCIAL', 'Condições Psicossociais'),
    ]
    TIPO_CHOICES = [
        ('FISICA', 'Física'), ('SENSORIAL', 'Sensorial'), 
        ('INTELECTUAL', 'Intelectual'), ('PSICOSSOCIAL', 'Psicossocial'), 
        ('MULTIPLA', 'Múltipla'), ('OUTRO', 'Outro')
    ]
    
    nome = models.CharField(max_length=100, unique=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, blank=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, blank=True)

    def __str__(self): return self.nome

class Gatilho(models.Model):
    CATEGORIA_CHOICES = [
        ('SAUDE_MENTAL', 'Saúde mental e sofrimento psicológico'),
        ('VIOLENCIA', 'Violência e abuso'),
        ('MEDICO', 'Contexto médico'),
        ('EXCLUSAO', 'Exclusão social'),
        ('OUTROS', 'Outros temas sensíveis'),
    ]
    
    nome = models.CharField(max_length=100, unique=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, blank=True)

    def __str__(self): return self.nome


class LibraryItem(TimeStampedModel):
    STATUS_CHOICES = [('PENDENTE', 'Pendente'), ('ATIVO', 'Aprovado'), ('REJEITADO', 'Rejeitado')]
    TIPO_CHOICES = [('FILME', 'Filme'), ('SERIE', 'Série'), ('LIVRO', 'Livro'), ('MUSICA', 'Música'), ('PODCAST', 'Podcast'), ('ARTIGO', 'Artigo')]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    motivo_rejeicao = models.TextField(blank=True, verbose_name="Motivo da Rejeição (Admin)")
    usuario_criador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='itens_cadastrados')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    ano_lancamento = models.PositiveIntegerField(null=True, blank=True)
    pais_origem = models.CharField(max_length=100, blank=True)
    idioma = models.CharField(max_length=50, blank=True)
    classificacao_indicativa = models.CharField(max_length=20, blank=True)
    capa = models.ImageField(upload_to='library/covers/', blank=True, null=True)
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
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(LibraryItem, on_delete=models.CASCADE, related_name='reviews')
    
    nota_geral = models.PositiveIntegerField(choices=RATING_CHOICES)
    nota_representatividade = models.PositiveIntegerField(choices=RATING_CHOICES)
    nota_critica = models.PositiveIntegerField(choices=RATING_CHOICES)
    
    comentario_justificativa = models.TextField(blank=True, verbose_name="Justificativa das notas")

    class Meta:
        unique_together = ('user', 'item')