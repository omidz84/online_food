from django.utils.translation import gettext as _

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serializers import AdminSerializer, AdminProfileSerializer
from user.models import MyUser
from user.validators import check_phone
from core.utils import translate

# ------------------------------------------------------------------------------------------

# Create your views here.


class AdminAPIView(APIView):
    serializer_class = AdminSerializer

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_phone_number = check_phone(serializer.validated_data["phone_number"])

        try:
            user = MyUser.objects.get(phone_number=serialized_phone_number)
            data = {
                "result": {
                    "user_id": user.id,
                    "user_type": user.type.title,
                    "phone_number": user.phone_number
                          },
                "Message": _("Login Successfully")
            }
            return Response(data=data, status=status.HTTP_200_OK)

        except MyUser.DoesNotExist:
            user = MyUser.objects.create(phone_number=serialized_phone_number)
            data = {
                "result": {
                    "user_id": user.id,
                    "user_type": user.type.title,
                    "phone_number": user.phone_number
                          },
                "Message": _("Registered Successfully")
            }
            return Response(data=data, status=status.HTTP_201_CREATED)


# ------------------------------------------------------------------------------------------


class AdminProfileAPIView(APIView):
    serializer_class = AdminProfileSerializer

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"Result": serializer.data, "Message": _("The Profile is Completed")},
                            status=status.HTTP_201_CREATED)

        return Response(data={"Message": _("Please Enter the Correct Information")}, status=status.HTTP_400_BAD_REQUEST)
