from django.http import HttpRequest
from django.shortcuts import render
from django.conf import settings

from utils.views import get_template

from . import urls
from . import forms
from .models import Photo, Category


def create_category(request: HttpRequest):
    template = get_template(app=urls.app_name)

    if request.method == 'GET':
        form = forms.CategoryForm
    
    if request.method == 'POST':
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            form = forms.CategoryForm()

    return render(request, template, {
        'form': form,
    })


def import_single_photo(request: HttpRequest):
    template = get_template(app=urls.app_name)

    if request.method == 'GET':
        form = forms.UploadPhotoForm()

    if request.method == 'POST':
        form = forms.UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = forms.UploadPhotoForm()

    return render(request, template, {
        'form': form,
    })


def display_all_photos(request: HttpRequest):
    template = get_template(app=urls.app_name)

    photos = Photo.objects.exclude(status=Photo.Status.DUPLICATED)

    photos_all = len(photos)

    no_category, created = Category.objects.get_or_create(name=settings.NO_CATEGORY_DIR)
    photos_no_category = len(Photo.objects.filter(category=no_category))

    duplicates, created = Category.objects.get_or_create(name=settings.DUPLICATES_DIR)
    photos_duplicates = len(Photo.objects.filter(category=duplicates))

    return render(request, template, {
        'photos_all': photos_all,
        'photos_no_category': photos_no_category,
        'photos_duplicates': photos_duplicates,
        'photos': photos,
    })


def display_duplicated_photos(request: HttpRequest):
    template = get_template(app=urls.app_name)

    duplicates = Photo.objects.filter(status=Photo.Status.DUPLICATED)

    return render(request, template, {
        'duplicates_num': len(duplicates),
        'duplicates': duplicates,
    })


def inspect_photo(request: HttpRequest, photo_name):
    template = get_template(app=urls.app_name)
    photo = Photo.objects.get(title=photo_name)

    # if request.method == 'GET':
    #     form = forms.UpdatePhotoForm(instance=photo)
    
    # if request.method == 'POST':
    #     form = forms.PhotoForm(request.POST, instance=photo)
    #     if form.is_valid():
    #         alter_photo = form.save(commit=False)
    #         photo.move_to_category(alter_photo.category.name)
    #         alter_photo.save()

    return render(request, template, {
        'photo': photo,
    })