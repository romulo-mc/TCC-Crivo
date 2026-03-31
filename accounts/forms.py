from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from .validators import SenhaForteValidator

STYLE_INPUT = {'class': 'form-control form-control-lg custom-input', 'style': 'border-radius: 15px; background-color: #E0F0F5; border: none;'}
STYLE_SELECT = {'class': 'form-select form-select-lg', 'style': 'border-radius: 15px; background-color: #E0F0F5; border: none; color: #333;'}
STYLE_CHECKBOX = {'class': 'form-check-input', 'style': 'width: 1.3em; height: 1.3em; margin-top: 0.2em;'}

class CadastroBasicoForm(forms.ModelForm):
    first_name = forms.CharField(label="Nome (Obrigatório)", widget=forms.TextInput(attrs=STYLE_INPUT))
    last_name = forms.CharField(label="Sobrenome (Obrigatório)", widget=forms.TextInput(attrs=STYLE_INPUT))
    username = forms.CharField(label="Usuário (Obrigatório)", widget=forms.TextInput(attrs=STYLE_INPUT))
    email = forms.EmailField(label="E-mail (Obrigatório)", widget=forms.EmailInput(attrs=STYLE_INPUT))
    email_confirmacao = forms.EmailField(label="Confirmar E-mail (Obrigatório)", widget=forms.EmailInput(attrs=STYLE_INPUT))
    password = forms.CharField(label="Senha (Obrigatório)", widget=forms.PasswordInput(attrs={**STYLE_INPUT, 'id': 'id_password_main'}), validators=[SenhaForteValidator()])
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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit: user.save()
        return user

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="Nome", required=False, widget=forms.TextInput(attrs=STYLE_INPUT))
    last_name = forms.CharField(label="Sobrenome", required=False, widget=forms.TextInput(attrs=STYLE_INPUT))
    username = forms.CharField(label="Nome de Usuário (@)", required=False, widget=forms.TextInput(attrs=STYLE_INPUT))

    genero = forms.ChoiceField(choices=UserProfile.GENERO_CHOICES, widget=forms.Select(attrs={**STYLE_SELECT, 'onchange': 'toggleOutro(this, "div_genero_outro")'}), label="Gênero (Obrigatório)")
    pronomes = forms.ChoiceField(choices=UserProfile.PRONOMES_CHOICES, widget=forms.Select(attrs={**STYLE_SELECT, 'onchange': 'toggleOutro(this, "div_pronomes_outro")'}), label="Pronomes (Obrigatório)")
    pais = forms.ChoiceField(choices=UserProfile.PAIS_CHOICES, widget=forms.Select(attrs=STYLE_SELECT), label="País (Obrigatório)")
    estado = forms.ChoiceField(choices=UserProfile.UF_CHOICES, widget=forms.Select(attrs=STYLE_SELECT), label="Estado/UF (Obrigatório)")
    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', **STYLE_INPUT}), label="Data de Nascimento (Obrigatório)")

    class Meta:
        model = UserProfile
        exclude = ('user', 'slug', 'modo_escuro', 'alto_contraste', 'fonte_tdah', 'fonte_dislexia', 'reduzir_animacoes', 'tamanho_fonte', 'receber_notificacoes', 'ocultar_avaliacoes')
        widgets = {
            'foto': forms.FileInput(attrs={'class': 'd-none', 'id': 'id_foto'}),
            'bio': forms.Textarea(attrs={'rows': 3, **STYLE_INPUT, 'placeholder': 'Conte um pouco sobre você...'}),
            'descricao_fisica': forms.Textarea(attrs={'rows': 3, **STYLE_INPUT, 'placeholder': 'Como você é visualmente?'}),
            'cid': forms.TextInput(attrs=STYLE_INPUT),
            'profissao': forms.TextInput(attrs=STYLE_INPUT),
            'conselho': forms.TextInput(attrs=STYLE_INPUT),
            'registro_profissional': forms.TextInput(attrs=STYLE_INPUT),
            'genero_outro': forms.TextInput(attrs={'placeholder': 'Especifique', **STYLE_INPUT}),
            'pronomes_outro': forms.HiddenInput(),
            'show_bio': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'is_pcd': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'is_profissional_saude': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'exibir_registro': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'is_aliado': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
            'tema_prefiro_nao': forms.CheckboxInput(attrs=STYLE_CHECKBOX),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['username'].initial = self.instance.user.username

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        if self.cleaned_data.get('first_name'): user.first_name = self.cleaned_data.get('first_name')
        if self.cleaned_data.get('last_name'): user.last_name = self.cleaned_data.get('last_name')
        if self.cleaned_data.get('username'): user.username = self.cleaned_data.get('username')
        if commit:
            user.save()
            profile.save()
        return profile

class AcessibilidadeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['modo_escuro', 'alto_contraste', 'fonte_dislexia', 'fonte_tdah', 'reduzir_animacoes', 'tamanho_fonte']
        widgets = {
            'modo_escuro': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'alto_contraste': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'fonte_dislexia': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'fonte_tdah': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'reduzir_animacoes': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'tamanho_fonte': forms.Select(attrs=STYLE_SELECT),
        }

class ConfiguracoesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['receber_notificacoes', 'ocultar_avaliacoes']
        widgets = {
            'receber_notificacoes': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'ocultar_avaliacoes': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }