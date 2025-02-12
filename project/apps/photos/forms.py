from django import forms
from . import models


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
        photo.title = photo.image.name

        if commit:
            photo.save()
        
        return photo