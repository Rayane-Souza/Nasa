from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página inicial
    path('api/get_asteroids/', views.AsteroideSearchView.as_view(), name='asteroid-search'),  # Busca geral
]
