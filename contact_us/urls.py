from django.urls import path
from .views import ContactUsAPIView

app_name = "contact_us"

urlpatterns = [
    path('', ContactUsAPIView.as_view(), name='contact-us'),
]