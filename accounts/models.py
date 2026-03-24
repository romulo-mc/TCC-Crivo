from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    PAIS_CHOICES = [
        ('BR', 'Brasil'), ('PT', 'Portugal'), ('US', 'Estados Unidos'), ('OUTRO', 'Outro'),
    ]

    UF_CHOICES = [
        ('', '---'), ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'), ('ESTR', 'Estrangeiro/Outro'),
    ]

    foto = models.ImageField(upload_to='perfil/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Sobre mim")
    descricao_fisica = models.TextField(blank=True, verbose_name="Descrição Física (Acessibilidade)")
    
    data_nascimento = models.DateField(null=True, blank=True)
    pais = models.CharField(max_length=100, choices=PAIS_CHOICES, default='BR', verbose_name="País")
    estado = models.CharField(max_length=25, choices=UF_CHOICES, blank=True, verbose_name="Estado/UF")

    GENERO_CHOICES = [
        ('M', 'Masculino'), ('F', 'Feminino'), ('NB', 'Não-binário'),
        ('PNA', 'Prefiro não informar'), ('OUTRO', 'Outro (Especificar)'),
    ]
    PRONOMES_CHOICES = [
        ('ELE', 'Ele/Dele'), ('ELA', 'Ela/Dela'), ('ELU', 'Elu/Delu'),
        ('QUALQUER', 'Qualquer um'), ('PNA', 'Prefiro não informar'), ('OUTRO', 'Outro (Especificar)'),
    ]

    genero = models.CharField(max_length=20, choices=GENERO_CHOICES, blank=True)
    genero_outro = models.CharField(max_length=50, blank=True)
    pronomes = models.CharField(max_length=20, choices=PRONOMES_CHOICES, blank=True)
    pronomes_outro = models.CharField(max_length=50, blank=True)

    tema_prefiro_nao = models.BooleanField(default=False, verbose_name="Prefiro não informar relação com o tema")
    
    is_pcd = models.BooleanField(default=False, verbose_name="Sou Pessoa com Deficiência")
    cid = models.CharField(max_length=50, blank=True, null=True, verbose_name="CID")

    is_profissional_saude = models.BooleanField(default=False, verbose_name="Profissional de Saúde")
    profissao = models.CharField(max_length=100, blank=True)
    conselho = models.CharField(max_length=50, blank=True)
    registro_profissional = models.CharField(max_length=50, blank=True)
    uf_registro = models.CharField(max_length=4, choices=UF_CHOICES, blank=True, verbose_name="UF do Conselho")
    exibir_registro = models.BooleanField(default=False)

    is_aliado = models.BooleanField(default=False, verbose_name="Aliado / Interessado")
    aliado_familiar = models.BooleanField(default=False)
    aliado_educador = models.BooleanField(default=False)
    aliado_estudante = models.BooleanField(default=False)
    aliado_apenas = models.BooleanField(default=False)
    
    show_bio = models.BooleanField(default=True)
    show_descricao_fisica = models.BooleanField(default=True)
    show_localizacao = models.BooleanField(default=True)
    show_genero = models.BooleanField(default=True)
    show_pronomes = models.BooleanField(default=True)

    FONTE_CHOICES = [('XP', 'Extra Pequena'), ('P', 'Pequena'), ('M', 'Média (Padrão)'), ('G', 'Grande'), ('XG', 'Extra Grande')]
    
    modo_escuro = models.BooleanField(default=False, verbose_name="Modo Escuro")
    alto_contraste = models.BooleanField(default=False, verbose_name="Alto Contraste")
    fonte_tdah = models.BooleanField(default=False, verbose_name="Fonte TDAH (Leitura Dinâmica)")
    fonte_dislexia = models.BooleanField(default=False, verbose_name="Fonte para Dislexia")
    reduzir_animacoes = models.BooleanField(default=False, verbose_name="Reduzir Animações (Motion)")
    tamanho_fonte = models.CharField(max_length=2, choices=FONTE_CHOICES, default='M', verbose_name="Tamanho da Fonte")  
    receber_notificacoes = models.BooleanField(default=True, verbose_name="Receber Notificações por E-mail")
    ocultar_avaliacoes = models.BooleanField(default=False, verbose_name="Ocultar minhas avaliações do Acervo no perfil público")

    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    @property
    def get_badges(self):
        badges = []
        if self.user.is_staff:
            badges.append({'nome': 'Crivo Oficial', 'cor': 'primary', 'icone': 'shield-check'})
        if self.is_pcd:
            nome_pcd = f'PCD (CID: {self.cid})' if self.cid else 'PCD'
            badges.append({'nome': nome_pcd, 'cor': 'info', 'icone': 'universal-access'})
        if self.is_profissional_saude and self.exibir_registro:
            badges.append({'nome': 'Profissional', 'cor': 'success', 'icone': 'heart-pulse'})
        if self.is_aliado:
            badges.append({'nome': 'Aliado', 'cor': 'secondary', 'icone': 'people'})
        return badges

    def save(self, *args, **kwargs):
        if not self.slug:
            nome_base = self.user.first_name if self.user.first_name else self.user.username
            slug_base = slugify(nome_base)
            if not slug_base:
                slug_base = 'usuario'
            self.slug = f"{slug_base}-{str(uuid.uuid4())[:6]}"
        super().save(*args, **kwargs)
    
@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        nome_base = instance.first_name if instance.first_name else 'usuario'
        slug_base = slugify(nome_base)
        slug_unico = f"{slug_base}-{str(uuid.uuid4())[:6]}"
        UserProfile.objects.create(user=instance, slug=slug_unico)

@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()