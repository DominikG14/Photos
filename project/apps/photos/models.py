from django.db import models
from django.conf import settings

import os
from enum import IntEnum


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class PhotoStatus(IntEnum):
    TRACKED = 0
    LOST = 1
    DUPLICATED = 2


def upload_to(instance, filename):
    return os.path.join(settings.MEDIA_ROOT, instance.category.name, filename)


class Photo(models.Model):
    PHOTO_STATUS = [
        (PhotoStatus.TRACKED, 'TRACKED'),
        (PhotoStatus.LOST, 'LOST'),
        (PhotoStatus.DUPLICATED, 'DUPLICATED')
    ]

    title = models.CharField(max_length=255, help_text='Custom name for a photo')
    filename = models.CharField(max_length=255, help_text='Original filename of the uploaded file')
    image = models.ImageField(upload_to=upload_to, help_text='Image path')
    status = models.IntegerField(choices=PHOTO_STATUS, default=PhotoStatus.TRACKED, help_text='State of a file detected by a system')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True, blank=True, help_text='Category that photo belongs to')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Time when photo was uploaded to a system')

    def save(self, *args, **kwargs):
        if Photo.objects.filter(filename=self.filename).exists():
            self.status = PhotoStatus.DUPLICATED
        
        if self.category is None:
            match self.status:
                case PhotoStatus.TRACKED:
                    no_category, created = Category.objects.get_or_create(name=settings.NO_CATEGORY_DIR)
                    self.category = no_category

                case PhotoStatus.DUPLICATED:
                    duplicates, created = Category.objects.get_or_create(name=settings.DUPLICATES_DIR)
                    self.category = duplicates

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.category.name} - {self.title}'