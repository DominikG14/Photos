from django.db import models


class Photo(models.Model):
    name = models.CharField(max_length=255)
    path = models.FilePathField()
    watched = models.BooleanField(default=True)