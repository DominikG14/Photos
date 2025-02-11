from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255)


class Photo(models.Model):
    EXTENSIONS = ('.png', '.jpg', '.jpeg')

    name = models.CharField(max_length=255)
    watched = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True, blank=True)

    def get_url(self):
        if self.category:
            return f'{settings.MEDIA_URL}/{self.category.name}/{self.name}'
        return f'{settings.NO_CATEGORY_URL}/{self.name}'
    
    def __str__(self):
        if self.category:
            return f'{self.category.name} - {self.name}'
        return f'{settings.NO_CATEGORY_NAME} - {self.name}'