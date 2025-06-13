from django import forms
from .models import Gift

class GiftForm(forms.ModelForm):
    STORE_TYPE_CHOICES = [
        ('physical', 'Loja Física'),
        ('online', 'Loja Online'),
    ]

    store_type = forms.ChoiceField(choices=STORE_TYPE_CHOICES, label="Tipo da Loja", widget=forms.RadioSelect)
    product_link = forms.URLField(label="Link do Produto", required=False, max_length=500)
    name = forms.CharField(label="Nome do Produto", max_length=255)
    photo = forms.ImageField(label="Foto do Produto", required=False)
    value = forms.DecimalField(label="Preço do Produto", max_digits=10, decimal_places=2)
    store_name = forms.CharField(label="Nome da Loja", max_length=255, required=False)

    class Meta:
        model = Gift
        fields = [
            'store_type',
            'product_link',
            'name',
            'photo',
            'value',
            'store_name',
            'anonymous_contributions',
        ]
