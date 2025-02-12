from django.db import models
from django.conf import settings

import shutil
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
    if instance.status == PhotoStatus.DUPLICATED:
        return os.path.join(settings.DUPLICATES_URL, filename)
    return os.path.join(settings.NO_CATEGORY_URL, filename)


class Photo(models.Model):
    PHOTO_STATUS = [
        (PhotoStatus.TRACKED, 'TRACKED'),
        (PhotoStatus.LOST, 'LOST'),
        (PhotoStatus.DUPLICATED, 'DUPLICATED')
    ]

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT)
    status = models.IntegerField(choices=PHOTO_STATUS, default=PhotoStatus.TRACKED)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if Photo.objects.filter(image=self.image.name).exists():
            self.status = PhotoStatus.DUPLICATED
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'