from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from . models import Cart, LogStatus, Status
from .serializers import CartAddSerializers

# Create your views here.


class AddToCartView(GenericAPIView):
    serializer_class = CartAddSerializers

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        food_id = serializer.validated_data['food_id']
        food_id = str(food_id)
        cart = request.session.get('cart', {})

        if food_id in cart:
            cart[food_id] += 1
        else:
            cart[food_id] = 1

        request.session['cart'] = cart
        request.session.modified = True

        return Response({'msg': 'OK'})
