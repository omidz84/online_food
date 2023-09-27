from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("code/", views.UserCodeAPIView.as_view(), name='user-code'),
    path("login-register/", views.UserAPIView.as_view(), name='user-login-register'),
    path("login-register/refresh/", views.UserCreateRefreshAPIView.as_view(), name='user-login-register-refresh-token'),
    path("profile/", views.UserProfileAPIView.as_view(), name="user-profile"),
    # path("profile/<slug:slug>/", views.UserProfileAPIView.as_view(), name="user-profile-slug"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="user-logout"),
    path('address/', views.AddressView.as_view(), name='Address_view')
]
