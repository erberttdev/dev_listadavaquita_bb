from django import forms

class GiftForm(forms.Form):
    name = forms.CharField(label="Nome do Presente", max_length=100)
    description = forms.CharField(label="Descrição", widget=forms.Textarea)
    price = forms.DecimalField(label="Preço", decimal_places=2)
