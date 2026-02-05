from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class CadastroBasicoForm(forms.ModelForm):
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirmacao = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="E-mail", required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Nome", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Sobrenome", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Usuário", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        senha1 = cleaned_data.get("password")
        senha2 = cleaned_data.get("password_confirmacao")
        if senha1 and senha2 and senha1 != senha2:
            self.add_error('password_confirmacao', "As senhas não conferem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Conte um pouco sobre você...'}),
            'descricao_fisica': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Ex: Homem branco, cabelos curtos...'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.TextInput(attrs={'class': 'form-control'}),
            'pronomes': forms.TextInput(attrs={'class': 'form-control'}),
            'cid': forms.TextInput(attrs={'class': 'form-control'}),
            'profissao': forms.TextInput(attrs={'class': 'form-control'}),
            'conselho': forms.TextInput(attrs={'class': 'form-control'}),
            'registro_profissional': forms.TextInput(attrs={'class': 'form-control'}),
            'uf_registro': forms.TextInput(attrs={'class': 'form-control'}),
        }