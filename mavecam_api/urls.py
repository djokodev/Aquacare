"""
Configuration des URLs principales - MAVECAM AquaCare API.

Structure de l'API:
- /admin/ : Interface d'administration Django pour équipe MAVECAM
- /api/accounts/ : Authentification et profils utilisateurs
- /api/aquaculture/ : Cycles de production et logs (Phase 2)
- /api/commerce/ : Catalogue et commandes (Phase 3)
- /api/support/ : Assistance technique (Phase 4)
- /api/education/ : Guides et formation (Phase 5)
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def api_root(request):
    """Endpoint racine fournissant les informations sur l'API."""
    return JsonResponse({
        'api': 'MAVECAM AquaCare API',
        'version': '1.0.0 MVP',
        'documentation': {
            'swagger': '/api/docs/',
            'redoc': '/api/redoc/',
            'schema': '/api/schema/',
        },
        'endpoints': {
            'accounts': '/api/accounts/',
            'admin': '/admin/',
        },
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    
    # Documentation Swagger/OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints
    path('api/accounts/', include('accounts.urls')),
    
    # Modules à venir :
    # path('api/aquaculture/', include('aquaculture.urls')),    # Phase 2
    # path('api/commerce/', include('commerce.urls')),          # Phase 3  
    # path('api/support/', include('support.urls')),            # Phase 4
    # path('api/education/', include('education.urls')),        # Phase 5
]
