from django.utils.translation import gettext as _

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from . models import Cart, LogStatus, Status
from user.models import MyUser, UserProfile
from food.models import Food
from .serializers import CartAddSerializers, SaveCartSerializers, ShowOrdersSerializers
from core.utils import translate

# Create your views here.


class AddToCartView(GenericAPIView):
    serializer_class = CartAddSerializers

    def post(self, request: Request):
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        food_id = serializer.validated_data['food_id']
        food_id = str(food_id)
        cart = request.session.get('cart', {})

        try:
            food = Food.objects.get(id=food_id)
            if food_id in cart:
                cart[food_id] += 1
                if cart[food_id] > food.count:
                    return Response({'msg': _('Quantity requested is more than stock')}, status.HTTP_400_BAD_REQUEST)
            else:
                cart[food_id] = 1
                if cart[food_id] > food.count:
                    return Response({'msg': _('Quantity requested is more than stock')}, status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'msg': _('food not found')}, status.HTTP_404_NOT_FOUND)

        request.session['cart'] = cart
        request.session.modified = True

        return Response({'msg': _('Add to cart')}, status.HTTP_201_CREATED)


class RemoveInCartView(GenericAPIView):
    serializer_class = CartAddSerializers

    def post(self, request: Request):
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        food_id = serializer.validated_data['food_id']
        food_id = str(food_id)
        cart = request.session.get('cart', {})
        try:
            if cart[food_id] > 1:
                cart[food_id] -= 1
            else:
                del cart[food_id]
        except:
            return Response({'msg': _('Not available in cart')}, status.HTTP_400_BAD_REQUEST)

        request.session['cart'] = cart
        request.session.modified = True

        return Response({'msg': _('Remove in cart')}, status.HTTP_200_OK)


class ShowCartView(GenericAPIView):
    queryset = Food.objects.all()

    def get(self, request: Request):
        translate(request)
        cart = request.session.get('cart', {})
        response_data = []
        final_price = 0
        for food_id, quantity in cart.items():
            try:
                food = Food.objects.get(id=food_id)
                response_data.append({
                    'food_id': food.id,
                    'food_name': food.name,
                    'food_price': food.price,
                    'food_count': food.count,
                    'image': '/media/' + str(food.image),
                    'quantity': quantity
                })
                final_price += food.price * quantity
            except Food.DoesNotExist:
                pass

        return Response({'foods': response_data, 'final price': final_price}, status.HTTP_200_OK)


class SaveCartView(GenericAPIView):
    serializer_class = SaveCartSerializers
    queryset = Cart.objects.all()

    def post(self, request: Request):
        translate(request)
        cart = request.session.get('cart')
        final_price = {}
        if not cart:
            return Response({'msg': _('The cart is empty')}, status=status.HTTP_400_BAD_REQUEST)
        for food_id, quantity in cart.items():
            try:
                food = Food.objects.get(id=food_id)
                final_price[food.id] = food.price
                food.count = food.count - quantity
                food.save()
            except Food.DoesNotExist:
                pass

        serializer = self.serializer_class(data={
            'user': request.data['user'],
            'foods': cart,
            'final_price': final_price
        })
        if serializer.is_valid():
            serializer.save()
            request.session.clear()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'msg': _('ERROR!!!')}, status=status.HTTP_400_BAD_REQUEST)


class ShowOrdersView(GenericAPIView):
    serializer_class = ShowOrdersSerializers
    queryset = Cart.objects.all()

    def post(self, request: Request):
        translate(request)
        try:
            carts = Cart.objects.filter(user=request.data['user_id'])
            a_carts = []
            for cart in carts:
                total_price = []
                foods = []
                for price, count in zip(cart.final_price.values(), cart.foods.values()):
                    final_price = price * count
                    total_price.append(final_price)

                for food_id, quantity in cart.foods.items():
                    food = Food.objects.get(id=food_id)
                    foods.append({
                        'food_id': food.id,
                        'food_name': food.name,
                        'food_price': cart.final_price[str(food.id)],
                        'food_count': food.count,
                        'image': '/media/' + str(food.image),
                        'category': food.category.title,
                        'quantity': quantity
                    })

                a_carts.append({
                    'user': cart.user.id,
                    'foods': foods,
                    'final_price': cart.final_price,
                    'total_price': sum(total_price),
                    'status': cart.status.status,
                    'created_at': cart.created_at
                })

            return Response({'carts': a_carts})
        except:
            return Response({'msg': _('ERROR!!!')}, status=status.HTTP_400_BAD_REQUEST)
