# translate
from django.utils.translation import activate

# swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


def translate(request):
    try:
        request.LANGUAGE_CODE = request.headers['Accept-Language']
        activate(request.LANGUAGE_CODE)
    except:
        request.LANGUAGE_CODE = 'en-us'


# swagger
schema_view = get_schema_view(
   openapi.Info(
      title="online food API",
      default_version='v1',
      description="online food",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

