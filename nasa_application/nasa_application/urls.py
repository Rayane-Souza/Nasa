# from django.contrib import admin
# from django.urls import path, include
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('asteroids.urls')),
#     # path('asteroids/', include('asteroids.urls')),
#     path('api/', include('asteroids.urls')),  

#     # Gerar o schema OpenAPI 3.0
#     path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),

#     # Swagger UI
#     path('swagger/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='swagger-ui'),
# ]


# from django.contrib import admin
# from django.urls import path, include
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('asteroids.urls')),  # Incluindo as URLs da aplicação 'asteroids'
#     path('api/', include('asteroids.urls')),  

#     path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
#     path('swagger/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='swagger-ui'),
# ]


# # nasa_application/urls.py
# from django.contrib import admin
# from django.urls import path, include
# from drf_spectacular.views import SpectacularSwaggerView
# from asteroids.views import index  # Importando a view index

# urlpatterns = [
#     # Página inicial mapeada para a URL raiz
#     path('', index, name='home'),  # A URL raiz agora exibe o index.html

#     # URL para o painel de administração
#     path('admin/', admin.site.urls),

#     # Incluindo as URLs da aplicação 'asteroids' com prefixo 'asteroids/'
#     path('asteroids/', include('asteroids.urls')),

#     # O Swagger UI, sem expor diretamente o endpoint `api/schema/`
#     path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
# ]

# from django.contrib import admin
# from django.urls import path
# from asteroids.views import (
#     AsteroideSearchView,
#     AsteroideListView,
#     AsteroideCreateView,
#     AsteroideDetailView,
#     index  # Importando a view index
# )
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# # Definindo a documentação do Swagger
# schema_view = get_schema_view(
#    openapi.Info(
#       title="API Asteroides",
#       default_version='v1',
#       description="Uma API para buscar e armazenar asteroides",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@asteroids.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
# )

# urlpatterns = [
#     path('admin/', admin.site.urls),  # URL para o admin
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Documentação Swagger

#     # Página inicial (index)
#     path('', index, name='index'),  # Adicionando a URL para a página inicial

#     # Rotas para a API de asteroides
#     path('api/asteroids/search/', AsteroideSearchView.as_view(), name='asteroid-search'),
#     path('api/asteroids/', AsteroideListView.as_view(), name='asteroid-list'),
#     path('api/asteroids/create/', AsteroideCreateView.as_view(), name='asteroid-create'),
#     path('api/asteroids/<int:pk>/', AsteroideDetailView.as_view(), name='asteroid-detail'),
# ]


from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuração do Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="API Asteroides",
      default_version='v1',
      description="API para gerenciar asteroides",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@asteroids.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include('asteroids.urls')),  # Inclui todas as URLs do app asteroids
]
