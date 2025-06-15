from django import forms
from .models import GiftListItem

class AddToGiftListForm(forms.ModelForm):
    class Meta:
        model = GiftListItem
        fields = []
