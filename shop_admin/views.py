from django.utils.translation import gettext as _

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .serializers import AdminSerializer, AdminProfileSerializer
from user.models import MyUser
from core.utils import translate
from user.validators import check_phone

# ---------------------------------------------------------------------------------

# Create your views here.


class AdminAPIView(APIView):
    serializer_class = AdminSerializer

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # We add the following code to validate the "phone number". 09130974226 is the same 9130974226.
        phone_number = check_phone(request.data["phone_number"])
        try:
            user = MyUser.objects.get(phone_number=phone_number)
            data = {
                "user_id": user.id,
                "phone_number": user.phone_number,
                "type": user.type.title,
                "Message": _("The user is already exists.")
            }
            return Response(data, status=status.HTTP_200_OK)

        except MyUser.DoesNotExist:
            user = MyUser.objects.create(phone_number=phone_number)
            data = {
                "user_id": user.id,
                "phone_number": user.phone_number,
                "type": user.type.title,
                "Message": _("The user registered successfully.")
            }
            return Response(data, status=status.HTTP_201_CREATED)

# ---------------------------------------------------------------------------------


class AdminProfileAPIView(APIView):
    serializer_class = AdminProfileSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Result": serializer.data, "Message": _("The User Profile is Complete")},
                        status=status.HTTP_201_CREATED)

