from django.urls import path
from . import views


app_name = 'photos'
urlpatterns = []


PATHS = [
    path('display-photos/', views.display_photos, name='display_photos'),
]


urlpatterns += PATHS