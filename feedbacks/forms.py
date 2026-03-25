from django import forms
from .models import BugReport, AvaliacaoPlataforma

class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ['descricao', 'print_tela', 'url_erro']
        widgets = {
            'descricao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Descreva detalhadamente o que aconteceu e como reproduzir o erro...'
            }),
            'print_tela': forms.FileInput(attrs={'class': 'form-control'}),
            'url_erro': forms.HiddenInput(),
        }

class AvaliacaoPlataformaForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoPlataforma
        exclude = ['usuario']
        widgets = {
            'nota_geral': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'nota_usabilidade': forms.Select(attrs={'class': 'form-select'}),
            'nota_acessibilidade': forms.Select(attrs={'class': 'form-select'}),
            'nota_design': forms.Select(attrs={'class': 'form-select'}),
            'probabilidade_recomendar': forms.Select(attrs={'class': 'form-select form-select-lg border-primary text-primary fw-bold'}),
            'feedback_aberto': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Conta pra gente o que você mais gostou ou o que podemos melhorar na plataforma!'
            }),
        }