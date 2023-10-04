from django.conf import settings
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from core.utils import translate

# Create your views here.


class RefreshTokenAnonymous(GenericAPIView):
    def get(self, request):
        translate(request)
        try:
            token = settings.REDIS_JWT_TOKEN.keys()[-1]
            return Response({'refresh': token}, status.HTTP_200_OK)
        except:
            return Response({'Token': [_('Token not found')]}, status.HTTP_400_BAD_REQUEST)
