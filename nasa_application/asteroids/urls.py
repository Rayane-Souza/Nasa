from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('get_asteroids/', views.get_asteroids, name='get_asteroids'),
]
