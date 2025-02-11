from django.http import HttpRequest
from django.shortcuts import render

from utils.views import get_template

from . import urls
from .models import Photo
from .utils import uncat



def display_photos(request: HttpRequest):
    template = get_template(app=urls.app_name)

    uncat.create_uncat_dir()
    uncat.move_uncat_files()
    return render(request, template, {})