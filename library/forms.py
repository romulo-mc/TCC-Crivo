from django import forms
from .models import LibraryItem, Categoria

class LibraryItemForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Tags (Condições e Gatilhos)"
    )

    class Meta:
        model = LibraryItem
        exclude = ['usuario_criador', 'status', 'criado_em', 'atualizado_em']
        
        widgets = {
            'sinopse': forms.Textarea(attrs={'rows': 3}),
            'descricao_detalhada_tema': forms.Textarea(attrs={'rows': 3}),
            'analise_critica': forms.Textarea(attrs={'rows': 3}),
            'elenco': forms.Textarea(attrs={'rows': 2}),
            'data_lancamento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if not isinstance(self.fields[field].widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            if isinstance(self.fields[field].widget, forms.CheckboxInput):
                self.fields[field].widget.attrs.update({'class': 'form-check-input'})