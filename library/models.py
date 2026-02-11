from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel

class Categoria(models.Model):
    TIPO_CHOICES = [
        ('CONDICAO', 'Condição / Deficiência'),
        ('GATILHO', 'Gatilho / Conteúdo Sensível'),
    ]
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    def __str__(self):
        return self.nome

class LibraryItem(TimeStampedModel):
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo/Visível'),
        ('MODERACAO', 'Em Moderação (Muitos deslikes)'),
        ('REJEITADO', 'Rejeitado'),
    ]
    
    TIPO_CHOICES = [
        ('LIVRO', 'Livro'),
        ('FILME', 'Filme/Série'),
        ('MUSICA', 'Música'),
        ('PODCAST', 'Podcast'),
        ('ARTIGO', 'Artigo'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    usuario_criador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='itens_cadastrados')
    
    # --- IDENTIFICAÇÃO BÁSICA ---
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200, verbose_name="Título")
    titulo_original = models.CharField(max_length=200, blank=True, verbose_name="Título Original")
    ano_lancamento = models.PositiveIntegerField(null=True, blank=True, verbose_name="Ano")
    pais_origem = models.CharField(max_length=100, blank=True, verbose_name="País de Origem")
    
    criador = models.CharField(max_length=200, verbose_name="Criador(es) / Autor / Diretor")
    
    capa = models.ImageField(upload_to='library/covers/', blank=True, null=True)
    link_acesso = models.URLField("Link para acessar (Netflix, PDF, YouTube...)", blank=True, null=True)
    
    sinopse = models.TextField(blank=True, verbose_name="Sinopse")
    
    # --- RELAÇÃO COM O TEMA ---
    tags = models.ManyToManyField(Categoria, blank=True, related_name='itens', verbose_name="Condições e Gatilhos")
    
    REPRESENTACAO_CHOICES = [
        ('PROTAGONISTA', 'Protagonista com deficiência'),
        ('SECUNDARIO', 'Personagem secundário'),
        ('TEMA_CENTRAL', 'Tema central'),
        ('SIMBOLICA', 'Representação simbólica'),
        ('OUTRO', 'Outro'),
    ]
    tipo_representacao = models.CharField(max_length=50, choices=REPRESENTACAO_CHOICES, blank=True)
    
    ABORDAGEM_CHOICES = [
        ('REALISTA', 'Realista'),
        ('INSPIRACIONAL', 'Inspiracional ("Superação")'),
        ('ESTEREOTIPADA', 'Estereotipada'),
        ('CRITICA', 'Crítica/Social'),
        ('MEDICA', 'Médica'),
        ('POLITICA', 'Política'),
    ]
    condicao_retratada = models.CharField(max_length=50, choices=ABORDAGEM_CHOICES, blank=True, verbose_name="A condição é retratada de forma")
    
    descricao_detalhada_tema = models.TextField(blank=True, verbose_name="Descrição detalhada da relação com o tema")
    
    analise_critica = models.TextField(blank=True, verbose_name="Análise Crítica (Combate ou reforça capacitismo?)")
    participacao_pcd = models.BooleanField(default=False, verbose_name="Existe participação de PcD na produção?")
    
    classificacao_etaria = models.CharField(max_length=20, blank=True, verbose_name="Faixa Etária")

    # --- CAMPOS ESPECÍFICOS---

    duracao = models.CharField(max_length=50, blank=True, help_text="Ex: 120 min ou 45 min/ep")
    genero = models.CharField(max_length=100, blank=True) # Ação, Drama...
    plataforma = models.CharField(max_length=200, blank=True, verbose_name="Nome da Plataforma (Ex: Netflix)")
    elenco = models.TextField(blank=True, verbose_name="Elenco Principal")
    ator_pcd_personagem_pcd = models.BooleanField(default=False, verbose_name="Ator PcD interpreta personagem PcD?")
    transcricao_disponivel = models.BooleanField(default=False, verbose_name="Transcrição disponível?")
    interprete_libras = models.BooleanField(default=False, verbose_name="Intérprete de Libras?")

    editora = models.CharField(max_length=100, blank=True)
    numero_paginas = models.PositiveIntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, blank=True, verbose_name="ISBN")
    doi = models.CharField(max_length=100, blank=True, verbose_name="DOI (Se acadêmico)")
    
    tem_audiobook = models.BooleanField(default=False)
    tem_braille = models.BooleanField(default=False)
    tem_ebook_acessivel = models.BooleanField(default=False)

    album = models.CharField(max_length=100, blank=True)
    letra_url = models.URLField(blank=True, verbose_name="Link para a letra")
    artista_pcd = models.BooleanField(default=False, verbose_name="O artista possui deficiência?")

    TIPO_ARTIGO_CHOICES = [
        ('ACADEMICO', 'Acadêmico'),
        ('JORNALISTICO', 'Jornalístico'),
        ('OPINATIVO', 'Opinativo'),
        ('RELATO', 'Relato Pessoal'),
    ]
    tipo_artigo_especifico = models.CharField(max_length=20, choices=TIPO_ARTIGO_CHOICES, blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"

    def update_status_based_on_votes(self):
        likes = self.votes.filter(voto=1).count()
        deslikes = self.votes.filter(voto=-1).count()
        if (deslikes - likes) >= 10:
            self.status = 'MODERACAO'
            self.save()

class ItemVote(TimeStampedModel):
    VOTO_CHOICES = [
        (1, 'Like / Útil'),
        (-1, 'Deslike / Problemático'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(LibraryItem, on_delete=models.CASCADE, related_name='votes')
    voto = models.IntegerField(choices=VOTO_CHOICES)

    class Meta:
        unique_together = ('user', 'item')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.item.update_status_based_on_votes()

class Review(TimeStampedModel):

    RATING_CHOICES = [(i, str(i)) for i in range(0, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(LibraryItem, on_delete=models.CASCADE, related_name='reviews')
    
    nota = models.PositiveIntegerField(choices=RATING_CHOICES, verbose_name="Nota Geral")
    
    crit_participacao = models.PositiveIntegerField(
        choices=RATING_CHOICES, default=0,
        verbose_name="Participação de PCD na produção",
        help_text="0: Nenhuma - 5: Protagonismo/Autoria/Consultoria direta"
    )
    
    crit_linguagem = models.PositiveIntegerField(
        choices=RATING_CHOICES, default=0,
        verbose_name="Linguagem adequada",
        help_text="0: Ofensiva/Datada - 5: Inclusiva/Correta"
    )
    
    crit_complexidade = models.PositiveIntegerField(
        choices=RATING_CHOICES, default=0,
        verbose_name="Complexidade da representação",
        help_text="0: Rasa/Unidimensional - 5: Profunda/Humanizada"
    )
    
    crit_modelo_social = models.PositiveIntegerField(
        choices=RATING_CHOICES, default=0,
        verbose_name="Modelo Médico vs Social",
        help_text="0: Foco total na cura/tragédia (Médico) - 5: Foco nas barreiras/sociedade (Social)"
    )
    
    crit_capacitismo = models.PositiveIntegerField(
        choices=RATING_CHOICES, default=0,
        verbose_name="Capacitismo explícito ou implícito",
        help_text="0: Inexistente/Crítica ao capacitismo - 5: Muito capacitista/Reforça preconceitos"
    )
    
    crit_lugar_fala = models.PositiveIntegerField(
        choices=RATING_CHOICES, default=0,
        verbose_name="Lugar de fala",
        help_text="0: Visão externa/estereotipada - 5: Narrativa construída por quem vivencia"
    )
    
    crit_superacao = models.PositiveIntegerField(
        choices=RATING_CHOICES, default=0,
        verbose_name="Narrativa de superação (Inspiration Porn)",
        help_text="0: Não utiliza esse tropo - 5: Baseado inteiramente em superação irreal"
    )
    
    crit_infantilizacao = models.PositiveIntegerField(
        choices=RATING_CHOICES, default=0,
        verbose_name="Infantilização",
        help_text="0: Tratamento adulto/adequado - 5: Extrema infantilização"
    )

    texto = models.TextField(verbose_name="Análise escrita")
    contem_spoiler = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'item')
        verbose_name = "Avaliação de Representatividade"
        verbose_name_plural = "Avaliações"

    def __str__(self):
        return f"Avaliação de {self.user} sobre {self.item}"
    
    contem_spoiler = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'item')