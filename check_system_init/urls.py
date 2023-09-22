from django.urls import path
from . import views


app_name = 'check_system_init'
urlpatterns = [
    path('anonymous/', views.RefreshTokenAnonymous.as_view(), name='token_anonymous')
]
