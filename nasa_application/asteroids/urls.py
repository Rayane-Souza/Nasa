from django.urls import path
from .views import AsteroideSearchView, AsteroideListView, AsteroideCreateView, AsteroideDetailView

urlpatterns = [
    # Rota para buscar asteroides na API da NASA (GET)
    path('asteroids/search/', AsteroideSearchView.as_view(), name='asteroid-search'),  
    
    # Rota para listar todos os asteroides locais (GET)
    path('asteroids/', AsteroideListView.as_view(), name='asteroid-list'),  
    
    # Rota para criar um novo asteroide (POST)
    path('asteroids/create/', AsteroideCreateView.as_view(), name='asteroid-create'),  
    
    # Rota para detalhes, atualização e exclusão de asteroides específicos (GET, PUT, DELETE)
    path('asteroids/<int:pk>/', AsteroideDetailView.as_view(), name='asteroid-detail'),
]
