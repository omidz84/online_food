from django.utils.translation import gettext as _

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serializers import AdminSerializer, AdminProfileSerializer, DeliverySerializer, DeliveryListSerializer, \
                         UpdateStatusDeliverySerializer
from user.models import MyUser, UserProfile
from user.validators import check_phone
from core.utils import translate
from .models import Delivery
from cart.models import CartItem, Cart, LogStatus, Status


# from cart.serializers import SaveCartSerializers, ShowOrdersPostSerializers

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
                "msg": _("Login Successfully")
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
                "msg": _("Registered Successfully")
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
            return Response(data={"Result": serializer.data, "msg": _("The Profile is Completed")},
                            status=status.HTTP_201_CREATED)

        return Response(data={"msg": _("Please Enter the Correct Information")}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------

# API 1:


class DeliveryAPIView(APIView):
    """
        This view is for "admin". In other words, this view displays the "names of deliverymen" and "customers' carts"
        to "admin".
    """
    serializer_class = DeliverySerializer

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

# ------------------------------------------------------------------------------------------

# API 2


class DeliveryListAPIView(APIView):
    """
        List all carts for each deliveryman.
    """
    serializer_class = DeliveryListSerializer

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        orders = Delivery.objects.filter(user=serializer.validated_data["user_id"])

        for cart in orders:
            items = Cart.objects.filter(id=cart.cart_id)

            all_item = []
            for item in items:
                all_item.append({
                     "cart": {
                         "id": item.id},
                     # customer
                     "user": {
                         "id": item.user.id,
                         "phone number": item.user.phone_number,
                         "address": item.address.address,
                     },
                     'status': {
                         "status": item.status.status,
                     },
                     "created_at": item.created_at
                 })

        return Response(data=all_item, status=status.HTTP_200_OK)


# ------------------------------------------------------------------------------------------

# API 3


class DeliveryDetailAPIView(APIView):
    """
    Retrieve a cart instance for each deliveryman. (Detail)
    """

    def get_object(self, id) -> Response:
        try:
            return Delivery.objects.get(id=id)
        except Delivery.DoesNotExist:
            return Response({"msg": _("There is no any Cart")})

    def get(self, request: Request, id) -> Response:
        translate(request)
        try:
            cart = self.get_object(id=id)
            item1 = Cart.objects.get(id=cart.cart_id)
            item2 = UserProfile.objects.get(user_id=item1.user.id)
            item3 = CartItem.objects.filter(cart_id=cart.cart_id)
            foods = []
            for item in item3:
                foods.append({
                    "id": item.food.id,
                    "name": item.food.name,
                    "image": '/media/' + str(item.food.image),
                    'category': item.food.category.title,
                    'quantity': item.quantity,
                })
            data = {
                "Cart": {
                    "cart_id": cart.cart_id,
                },
                "User": {
                    "user_id": item1.user.id,
                    "user_name": item2.last_name,
                    "user_phone_number": item1.user.phone_number,
                    "address": item1.address.address,
                    "location": item1.address.location,
                },
                "Foods": {
                    'food': foods
                },
                "Status": {
                    "status": item1.status.status
                },
                "created_at": item1.created_at
                            }
            return Response(data={"Result": data}, status=status.HTTP_200_OK)
        except:
            return Response(data={"msg": _("This delivery id does not exist.")}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------

# API 4


class UpdateStatusDeliveryAPIView(GenericAPIView):
    serializer_class = UpdateStatusDeliverySerializer
    queryset = Delivery.objects.all()

    def patch(self, request: Request, *args, **kwargs):
        translate(request)
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance=instance, data=request.data)
            serializer.is_valid()
            serializer.save()
            cart = Cart.objects.get(id=serializer.data['cart'])
            cart.status = Status.objects.get(id=4)
            cart.save()
            print(cart.status)
            LogStatus.objects.create(cart_id=cart.id, status_id=cart.status_id)
            return Response(data={"msg": _("Successfully Done")}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(data={"msg": _("Error")}, status=status.HTTP_400_BAD_REQUEST)



