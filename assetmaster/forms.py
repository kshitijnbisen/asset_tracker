from django import forms
from .models import AssetType,Item

class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields = "__all__"


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"