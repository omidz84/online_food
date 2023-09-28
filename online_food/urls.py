from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# swagger
from core.utils import schema_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', include('check_system_init.urls')),
    path('api/user/', include("user.urls")),
    path('api/food/', include('food.urls')),

    # swagger
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns = urlpatterns+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
