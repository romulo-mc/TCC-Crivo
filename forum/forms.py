from django import forms
from .models import Topico, Resposta

class TopicoForm(forms.ModelForm):
    class Meta:
        model = Topico
        fields = ['titulo', 'categoria', 'outra_categoria', 'conteudo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dê um título claro para a discussão'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Relate sua experiência ou dúvida...'}),
            'outra_categoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Qual a categoria?',
                'aria-label': 'Especifique a outra categoria'
            }),
        }
        labels = {
            'titulo': 'Título da Discussão',
            'conteudo': 'Conteúdo (Seja detalhado)',
        }

class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['conteudo']