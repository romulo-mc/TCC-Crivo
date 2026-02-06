from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

STYLE_INPUT = {
    'class': 'form-control form-control-lg', 
    'style': 'border-radius: 15px; background-color: #E0F0F5; border: none;'
}

STYLE_SELECT = {
    'class': 'form-select form-select-lg', 
    'style': 'border-radius: 15px; background-color: #E0F0F5; border: none; color: #333;'
}

STYLE_CHECKBOX = {
    'class': 'form-check-input', 
    'style': 'width: 1.3em; height: 1.3em; margin-top: 0.2em;'
}

class CadastroBasicoForm(forms.ModelForm):
    first_name = forms.CharField(label="Nome (Obrigatório)", widget=forms.TextInput(attrs=STYLE_INPUT))
    last_name = forms.CharField(label="Sobrenome (Obrigatório)", widget=forms.TextInput(attrs=STYLE_INPUT))
    username = forms.CharField(label="Usuário (Obrigatório)", widget=forms.TextInput(attrs=STYLE_INPUT))
    email = forms.EmailField(label="E-mail (Obrigatório)", widget=forms.EmailInput(attrs=STYLE_INPUT))
    email_confirmacao = forms.EmailField(label="Confirmar E-mail (Obrigatório)", widget=forms.EmailInput(attrs=STYLE_INPUT))
    password = forms.CharField(label="Senha (Obrigatório)", widget=forms.PasswordInput(attrs=STYLE_INPUT))
    password_confirmacao = forms.CharField(label="Confirmar Senha (Obrigatório)", widget=forms.PasswordInput(attrs=STYLE_INPUT))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirmacao"):
            self.add_error('password_confirmacao', "As senhas não conferem.")
        if cleaned_data.get("email") != cleaned_data.get("email_confirmacao"):
            self.add_error('email_confirmacao', "Os e-mails não conferem.")
        return cleaned_data

class UserProfileForm(forms.ModelForm):    
    genero = forms.ChoiceField(choices=UserProfile.GENERO_CHOICES, widget=forms.Select(attrs={**STYLE_SELECT, 'onchange': 'toggleOutro(this, "div_genero_outro")'}), label="Gênero (Obrigatório)")
    pronomes = forms.ChoiceField(choices=UserProfile.PRONOMES_CHOICES, widget=forms.Select(attrs={**STYLE_SELECT, 'onchange': 'toggleOutro(this, "div_pronomes_outro")'}), label="Pronomes (Obrigatório)")
    
    pais = forms.ChoiceField(choices=UserProfile.PAIS_CHOICES, widget=forms.Select(attrs=STYLE_SELECT), label="País (Obrigatório)")
    estado = forms.ChoiceField(choices=UserProfile.UF_CHOICES, widget=forms.Select(attrs=STYLE_SELECT), label="Estado/UF (Obrigatório)")
    
    uf_registro = forms.ChoiceField(choices=UserProfile.UF_CHOICES, widget=forms.Select(attrs=STYLE_SELECT), required=False, label="UF do Conselho")

    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', **STYLE_INPUT}), label="Data de Nascimento (Obrigatório)")

    class Meta:
        model = UserProfile
        exclude = ('user',)
        
        widgets = {
            'foto': forms.FileInput(attrs={'class': 'd-none', 'id': 'id_foto'}),
            'bio': forms.Textarea(attrs={'rows': 3, **STYLE_INPUT, 'placeholder': 'Conte um pouco sobre você...'}),
            'descricao_fisica': forms.Textarea(attrs={'rows': 3, **STYLE_INPUT, 'placeholder': 'Como você é visualmente? (Para leitores de tela)'}),
            'cid': forms.TextInput(attrs=STYLE_INPUT),
            'profissao': forms.TextInput(attrs=STYLE_INPUT),
            'conselho': forms.TextInput(attrs=STYLE_INPUT),
            'registro_profissional': forms.TextInput(attrs=STYLE_INPUT),
            'genero_outro': forms.TextInput(attrs={'placeholder': 'Digite seu gênero', **STYLE_INPUT}),
            'pronomes_outro': forms.HiddenInput(),
            
            'show_bio': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'show_descricao_fisica': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'show_localizacao': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'show_genero': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'show_pronomes': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            
            'is_pcd': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'is_profissional_saude': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'exibir_registro': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            
            'is_aliado': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'aliado_familiar': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'aliado_educador': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'aliado_estudante': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'aliado_apenas': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'tema_prefiro_nao': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
        }