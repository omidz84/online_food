from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request

from django.utils.translation import gettext as _
from .models import ContactUs
from .serializers import ContactUsSerializer
from core.utils import translate


class ContactUsAPIView(APIView):
    """
    List all comments, or create a new comment.
    """

    serializer_class = ContactUsSerializer

    def get(self, request: Request) -> Response:
        translate(request)
        comments = ContactUs.objects.all().order_by('-created_at')
        serializer = self.serializer_class(instance=comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Result": serializer.data, "Message": _("The operation is successful")},
                       status=status.HTTP_201_CREATED)

        return Response({"Message": _('pleas enter correct information')}, status=status.HTTP_400_BAD_REQUEST)

        # --------------------------------------------------------------------------------
#
# class ContactUs1APIView(ListCreateAPIView):
#     queryset = ContactUs.objects.all().order_by('-created_at')
#     serializer_class = ContactUsSerializer
#     # permission_classes = [IsAdminUser]
#
#     def list(self, request: Request) -> Response:
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(instance=queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def create(self, request: Request) -> Response:
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'Result': serializer.data, 'msg': 'operation is successful'}, status=status.HTTP_201_CREATED)


#
#     def list(self, request, *args, **kwargs):
#         translate(request)
#         queryset = self.get_queryset()
#         serializer_class = self.serializer_class(queryset, many=True)
#         return Response(serializer_class.data, status.HTTP_200_OK)
#
#     def create(self, request, *args, **kwargs):
#         translate(request)
#         # queryset = self.get_queryset()
#         serializer_class = self.serializer_class(request.data)
#         return Response(serializer_class.data, status.HTTP_201_CREATED)
#
#
