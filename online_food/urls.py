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
    path('api/user/', include("user.urls", namespace="user")),
    path('api/food/', include('food.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/contact-us/', include('contact_us.urls', namespace="contact_us")),
    path('api/shop-admin/', include('shop_admin.urls', namespace="shop_admin")),


    # swagger
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]

urlpatterns = urlpatterns+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
