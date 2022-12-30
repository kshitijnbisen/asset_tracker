from django import forms
from .models import AssetType, Item, AssetImage

class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields = "__all__"


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"


class AssetImageForm(forms.ModelForm):
    images = forms.ImageField(required=False,widget=forms.FileInput(attrs={"class": "form-control", "multiple": True}))

    class Meta:
        model = AssetImage
        fields = ['images']