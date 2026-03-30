import difflib
from django import forms
from .models import LibraryItem, Review, Condicao, Gatilho

class LibraryItemForm(forms.ModelForm):
    condicoes = forms.ModelMultipleChoiceField(
        queryset=Condicao.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select select2', 'data-placeholder': 'Pesquise as condições...'})
    )
    gatilhos = forms.ModelMultipleChoiceField(
        queryset=Gatilho.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select select2', 'data-placeholder': 'Pesquise os gatilhos...'})
    )

    tipo_representacao = forms.ChoiceField(
        choices=[('', '---------')] + LibraryItem.TIPO_REP_CHOICES,
        required=False,
        widget=forms.Select()
    )
    abordagem = forms.ChoiceField(
        choices=[('', '---------')] + LibraryItem.ABORDAGEM_CHOICES,
        required=False,
        widget=forms.Select()
    )
    combate_ou_reforca = forms.ChoiceField(
        choices=[('', '---------')] + LibraryItem.COMBATE_REFORCA,
        required=False,
        widget=forms.Select()
    )

    class Meta:
        model = LibraryItem
        exclude = ['status', 'usuario_criador']
        labels = {
            'combate_ou_reforca': 'Impacto da Obra (Em relação ao Capacitismo):',
            'alt_text': 'Descrição da Imagem (Texto Alternativo para Cegos/Baixa Visão):',
            'capa': 'Capa/Pôster da Obra:',
            'titulo': 'Título da Obra:',
        }
        widgets = {
            'sinopse': forms.Textarea(attrs={'rows': 3}),
            'elenco_principal': forms.Textarea(attrs={'rows': 2}),
            'descricao_representacao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descreva a representação com suas palavras...'}),
            'analise_critica': forms.Textarea(attrs={'rows': 3, 'placeholder': 'O que você achou dessa abordagem?'}),
            'pontos_positivos': forms.Textarea(attrs={'rows': 2}),
            'pontos_problematicos': forms.Textarea(attrs={'rows': 2}),
            'alt_text': forms.TextInput(attrs={'placeholder': 'Ex: Pôster do filme mostrando um homem em uma cadeira de rodas olhando para o mar...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            widget = field.widget
            
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, forms.Select) and not isinstance(widget, forms.SelectMultiple):
                widget.attrs['class'] = 'form-select'
            elif not isinstance(widget, (forms.RadioSelect, forms.SelectMultiple)):
                widget.attrs['class'] = 'form-control'
        
        if 'tipo_representacao_outro' in self.fields:
            self.fields['tipo_representacao_outro'].widget.attrs['placeholder'] = 'Especifique o tipo de representação...'
        if 'abordagem_outro' in self.fields:
            self.fields['abordagem_outro'].widget.attrs['placeholder'] = 'Especifique a abordagem...'

    def clean_descricao_representacao(self):
        texto_novo = self.cleaned_data.get('descricao_representacao')
        if not texto_novo: 
            return texto_novo

        textos_existentes = LibraryItem.objects.exclude(descricao_representacao="").values_list('descricao_representacao', flat=True)
        
        for texto_antigo in textos_existentes:
            similaridade = difflib.SequenceMatcher(None, texto_novo.lower(), texto_antigo.lower()).ratio()
            if similaridade > 0.8:
                raise forms.ValidationError("Este texto é muito parecido com uma análise já cadastrada no Acervo. Por favor, escreva com suas próprias palavras.")
        
        return texto_novo


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['nota_geral', 'nota_representatividade', 'nota_critica', 'comentario_justificativa']
        widgets = {
            'nota_geral': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'nota_representatividade': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'nota_critica': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'comentario_justificativa': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Justifique suas notas rapidamente (Opcional)'}),
        }