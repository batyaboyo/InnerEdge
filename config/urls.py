from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('', RedirectView.as_view(url='/api/docs/', permanent=False), name='root'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/accounts/', include('accounts.urls')),
    path('api/market/', include('market.urls')),
    path('api/journal/', include('journal.urls')),
    path('api/intel/', include('intel.urls')),
    path('api/paper/', include('paper.urls')),
    path('api/alerts/', include('alerts.urls')),
    path('api/billing/', include('billing.urls')),
]
