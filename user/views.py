from django.utils.translation import gettext as _

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AddressSerializers
from core.utils import translate


class AddressView(GenericAPIView):
    serializer_class = AddressSerializers

    def post(self, request):
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
