from django import forms
from .models import RecursoEducativo

class RecursoEducativoForm(forms.ModelForm):
    class Meta:
        model = RecursoEducativo
        fields = ['titulo', 'tipo', 'descricao', 'arquivo', 'capa', 'codigo_incorporacao', 'url_externa']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Guia Prático de Acessibilidade'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Legenda do post...'}),
            'arquivo': forms.FileInput(attrs={'class': 'form-control'}),
            'capa': forms.FileInput(attrs={'class': 'form-control'}),
            'codigo_incorporacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '<iframe src="..."></iframe>'}),
            'url_externa': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }