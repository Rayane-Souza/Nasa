# from django.urls import path
# from .views import AsteroideSearchView, AsteroideListView, AsteroideCreateView, AsteroideDetailView
# from django.urls import path
# from . import views

# urlpatterns = [
#     # Rota para buscar asteroides na API da NASA (GET)
#     path('asteroids/search/', AsteroideSearchView.as_view(), name='asteroid-search'),  
    
#     # Rota para listar todos os asteroides locais (GET)
#     path('asteroids/', AsteroideListView.as_view(), name='asteroid-list'),  
    
#     # Rota para criar um novo asteroide (POST)
#     path('asteroids/create/', AsteroideCreateView.as_view(), name='asteroid-create'),  
    
#     # Rota para detalhes, atualização e exclusão de asteroides específicos (GET, PUT, DELETE)
#     path('asteroids/<int:pk>/', AsteroideDetailView.as_view(), name='asteroid-detail'),
   
# ]

    
from django.urls import path
from . import views
from .views import AsteroideSearchView, AsteroideListView, AsteroideCreateView, AsteroideDetailView

urlpatterns = [
    # Página inicial
    path('', views.index, name='index'),
    
    # Rota para a função verificar_asteroide
    path('verificar_asteroide/', views.verificar_asteroide, name='verificar_asteroide'),

    # Rotas para APIs baseadas em classe
    path('api/asteroids/search/', AsteroideSearchView.as_view(), name='asteroid-search'),
    path('api/asteroids/', AsteroideListView.as_view(), name='asteroid-list'),
    path('api/asteroids/create/', AsteroideCreateView.as_view(), name='asteroid-create'),
    path('api/asteroids/<int:pk>/', AsteroideDetailView.as_view(), name='asteroid-detail'),
]



