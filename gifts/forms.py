from django import forms
from .models import GiftListItem, Gift

class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ['name', 'value', 'store_name', 'store_type', 'store_address_or_link', 'photo', 'product_link', 'priority', 'allow_simultaneous_contributions']

class AddToGiftListForm(forms.ModelForm):
    class Meta:
        model = GiftListItem
        fields = []
