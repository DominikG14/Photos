from django.db import models
from django.conf import settings

import shutil
import os


class Category(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"



class Photo(models.Model):
    EXTENSIONS = ('.png', '.jpg', '.jpeg')

    name = models.CharField(max_length=255, primary_key=True)
    watched = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True, blank=True)

    def get_url(self):
        if self.category:
            return f'{settings.MEDIA_URL}/{self.category.name}/{self.name}'
        return f'{settings.NO_CATEGORY_URL}/{self.name}'
    
    def move_to_category(self, dest_dir):
        src_file_path = self.get_url()

        if dest_dir == settings.NO_CATEGORY_NAME:
            dest_file_path = os.path.join(settings.NO_CATEGORY_ROOT, self.name)
        else:
            dest_file_path = os.path.join(settings.WITH_CATEGORY_ROOT, self.category.name, self.name)

        try:
            shutil.move(src_file_path, dest_file_path)
            print(f"Moved: {src_file_path} -> {dest_file_path}")
        except shutil.Error as e:
            print(f"Error moving {src_file_path}: {e}")

    def __str__(self):
        if self.category:
            return f'{self.category.name} - {self.name}'
        return f'{settings.NO_CATEGORY_NAME} - {self.name}'