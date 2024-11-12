from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('asteroids.urls')),
    # path('asteroids/', include('asteroids.urls')),
    path('api/', include('asteroids.urls')),  

    # Gerar o schema OpenAPI 3.0
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),

    # Swagger UI
    path('swagger/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='swagger-ui'),
]
