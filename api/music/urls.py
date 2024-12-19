from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('test', views.get_artists, name='get_items_raw'),
    path('tracks', views.get_tracks, name='get_tracks'),
    path('popular', views.get_most_popular, name='get_most_popular'),
    path('longest_loudest', views.get_longest_loudest, name='get_longest_loudest'),
]
