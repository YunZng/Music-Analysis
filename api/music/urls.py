from django.urls import path
from . import views
# from other_app.views import Home


urlpatterns = [
    path('', views.home, name='home')
]
