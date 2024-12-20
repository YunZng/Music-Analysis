from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('test', views.get_artists, name='get_items_raw'),
    path('tracks', views.get_tracks, name='get_tracks'),
    path('popular', views.get_most_popular, name='get_most_popular'),
    path('longest_loudest', views.get_longest_loudest, name='get_longest_loudest'),
    path('analysis', views.get_analysis, name='get_analysis'),
    path('recommendation', views.get_predict_recommand, name='get_recommendations'),
    path('rating', views.get_predict_rating, name='get_predictions'),
    path('custom_query1', views.get_custom_query1, name='get_custom_query1'),
    path('custom_query2', views.get_custom_query2, name='get_custom_query2'),
    path('custom_query3', views.get_custom_query3, name='get_custom_query3'),
    path('custom_query4', views.get_custom_query4, name='get_custom_query4'),
    path('custom_query', views.get_custom_query, name='get_custom_query')
]
