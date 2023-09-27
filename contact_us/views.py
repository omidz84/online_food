# from rest_framework.generics import ListCreateAPIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import ContactUs
# from .serializers import ContactUsSerializer
# from core.utils import translate
#
#
# class ContactUsAPIView(ListCreateAPIView):
#     queryset = ContactUs.objects.all().order_by('-created_at')
#     serializer_class = ContactUsSerializer
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
