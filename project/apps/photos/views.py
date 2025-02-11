from django.http import HttpRequest
from django.shortcuts import render

from utils.views import get_template

from . import urls
from .models import Photo
from .utils.no_category import NoCategoryPhotos


def import_photos(request: HttpRequest):
    template = get_template(app=urls.app_name)

    ncp = NoCategoryPhotos()

    ncp.create_dir()
    ncp.move_files()
    return render(request, template, {})


def display_photos(request: HttpRequest):
    template = get_template(app=urls.app_name)

    photos = Photo.objects.all()

    return render(request, template, {
        'photos': photos,
    })