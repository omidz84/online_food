from django.urls import path
from .views import AdminAPIView, AdminProfileAPIView

app_name = "shop_admin"

urlpatterns = [
    path("login-register/", AdminAPIView.as_view(), name="admin-login-register"),
    path("profile/", AdminProfileAPIView.as_view(), name="admin-profile"),
]