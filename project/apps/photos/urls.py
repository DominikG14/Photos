from django.urls import path
from . import views


app_name = 'photos'
urlpatterns = []


PATHS = [
    path('import/single/', views.import_single_photo, name='import_single_photo'),
    path('display/all/', views.display_all_photos, name='display_all_photos'),
    path('display/duplicated/', views.display_duplicated_photos, name='display_duplicated_photos'),
    path('display/<photo_name>/', views.inspect_photo, name='inspect_photo'),
    path('categories/create/', views.create_category, name='create_category'),
]


urlpatterns += PATHS