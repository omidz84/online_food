from django.urls import path
from .views import AdminAPIView, AdminProfileAPIView, DeliveryAPIView, DeliveryListAPIView, DeliveryDetailAPIView, \
                   UpdateStatusDeliveryAPIView

app_name = "shop-admin"

urlpatterns = [
    path("login-register/", AdminAPIView.as_view(), name="admin-login-register"),
    path("profile/", AdminProfileAPIView.as_view(), name="admin-profile"),
    path('delivery/', DeliveryAPIView.as_view(), name='admin-delivery'),
    path('delivery/list/', DeliveryListAPIView.as_view(), name='delivery-list'),
    path('delivery/detail/<int:id>/', DeliveryDetailAPIView.as_view(), name='delivery-detail'),
    path('delivery/update-status/<int:pk>/', UpdateStatusDeliveryAPIView.as_view(), name="delivery-update-status"),
]

