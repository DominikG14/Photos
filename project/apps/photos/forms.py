from django import forms
from . import models


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name']
        labels = {
            'name': 'Nazwa Kategorii',
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = '__all__'
        labels = {
            'category': 'Kategoria',
        }