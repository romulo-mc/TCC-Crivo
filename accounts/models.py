from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # --- Identidade & Visual ---
    foto = models.ImageField(upload_to='perfil/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Sobre mim")
    descricao_fisica = models.TextField(blank=True, verbose_name="Descrição Física (Acessibilidade)")
    
    # --- Localização & Demografia ---
    pais = models.CharField(max_length=100, blank=True, verbose_name="País")
    estado = models.CharField(max_length=100, blank=True, verbose_name="Estado")
    
    data_nascimento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=50, blank=True, verbose_name="Gênero")
    genero_outro = models.CharField(max_length=50, blank=True, verbose_name="Gênero (Outro)")
    pronomes = models.CharField(max_length=50, blank=True, verbose_name="Pronomes")

    # --- Relação com o Tema ---
    is_pcd = models.BooleanField(default=False, verbose_name="Sou Pessoa com Deficiência")
    cid = models.CharField(max_length=20, blank=True, null=True, verbose_name="CID (Opcional)")

    is_profissional_saude = models.BooleanField(default=False, verbose_name="Profissional de Saúde")
    # Campos exclusivos do Profissional
    profissao = models.CharField(max_length=100, blank=True)
    conselho = models.CharField(max_length=50, blank=True) # Ex: CRM, CRP
    registro_profissional = models.CharField(max_length=50, blank=True, verbose_name="Nº Registro")
    uf_registro = models.CharField(max_length=2, blank=True, verbose_name="UF do Registro")
    exibir_registro = models.BooleanField(default=False, verbose_name="Exibir registro no perfil?")

    # Outras categorias
    is_familiar = models.BooleanField(default=False, verbose_name="Familiar / Cuidador")
    is_educador = models.BooleanField(default=False, verbose_name="Educador / Pesquisador")
    is_estudante = models.BooleanField(default=False, verbose_name="Estudante")
    is_aliado = models.BooleanField(default=False, verbose_name="Aliado / Interessado")

    # --- 4. Configurações de Privacidade ---
    show_badges = models.BooleanField(default=True, verbose_name="Mostrar Badges")
    show_bio = models.BooleanField(default=True, verbose_name="Mostrar Bio")
    show_descricao_fisica = models.BooleanField(default=True, verbose_name="Mostrar Desc. Física")
    show_localizacao = models.BooleanField(default=True, verbose_name="Mostrar Localização")
    show_idade = models.BooleanField(default=False, verbose_name="Mostrar Faixa Etária")
    show_genero = models.BooleanField(default=True, verbose_name="Mostrar Gênero")
    show_pronomes = models.BooleanField(default=True, verbose_name="Mostrar Pronomes")

    def __str__(self):
        return f"Perfil de {self.user.username}"