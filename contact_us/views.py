from django.utils.translation import gettext as _

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .models import ContactUs
from .serializers import ContactUsSerializer
from core.utils import translate


class ContactUsAPIView(APIView):
    serializer_class = ContactUsSerializer

    def get(self, request: Request) -> Response:
        translate(request)
        comments = ContactUs.objects.all().order_by("-created_at")
        serializer = self.serializer_class(instance=comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"Result": serializer.validated_data,
                                  "Message": _("The Operation Completed Successfully")}, status=status.HTTP_201_CREATED)
        return Response(data={"Message": _("Please Enter Correct Information.")}, status=status.HTTP_400_BAD_REQUEST)
