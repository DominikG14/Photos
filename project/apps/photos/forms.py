from django import forms
from . import models

import os


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name']
        labels = {
            'name': 'Nazwa Kategorii',
        }


class UploadPhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image']
        labels = {}
    
    def save(self, commit: bool = True):
        photo = super().save(commit=False)

        photo.filename = photo.image.name
        photo.title, extension = os.path.splitext(photo.filename)

        if commit:
            photo.save()
        
        return photo