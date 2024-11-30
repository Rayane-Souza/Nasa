# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.index, name='index'),  # Página inicial
#     path('api/get_asteroids/', views.AsteroideSearchView.as_view(), name='asteroid-search'),  # Busca geral
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # A página inicial agora é mapeada para o index
    path('api/get_asteroids/', views.AsteroideSearchView.as_view(), name='asteroid-search'),
]
