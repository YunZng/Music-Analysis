from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('test', views.get_artists, name='get_items_raw'),
    path('tracks', views.get_tracks, name='get_tracks'),
]
