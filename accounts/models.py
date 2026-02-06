from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    
    PAIS_CHOICES = [
        ('BR', 'Brasil'),
        ('PT', 'Portugal'),
        ('US', 'Estados Unidos'),
        ('OUTRO', 'Outro'),
    ]

    UF_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
        ('ESTR', 'Estrangeiro/Outro'),
    ]

    # --- Identidade & Visual ---
    foto = models.ImageField(upload_to='perfil/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Sobre mim")
    descricao_fisica = models.TextField(blank=True, verbose_name="Descrição Física (Acessibilidade)")
    
    # --- Localização & Demografia ---
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

    # --- Relação com o Tema ---
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

    # --- Privacidade ---
    show_bio = models.BooleanField(default=True)
    show_descricao_fisica = models.BooleanField(default=True)
    show_localizacao = models.BooleanField(default=True)
    show_genero = models.BooleanField(default=True)
    show_pronomes = models.BooleanField(default=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"