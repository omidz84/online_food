from django.utils.translation import gettext as _

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from . models import Cart, CartItem
from food.models import Food
from .serializers import CartAddSerializers,\
    SaveCartSerializers,\
    ShowOrdersSerializers, \
    ShowOrdersPostSerializers
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

        try:
            serializers = self.serializer_class(data=request.data)
            serializers.is_valid()
            serializers.save()
            carts = request.session.get('cart')
            for food, quantity in carts.items():
                food = Food.objects.get(id=food)
                if food.count > quantity:
                    CartItem.objects.create(cart_id=serializers.data['id'],
                                            food_id=food.id,
                                            quantity=quantity,
                                            price=food.price
                                            )
                    food.count = food.count - quantity
                    food.save()
                else:
                    Cart.objects.get(id=serializers.data['id']).delete()
                    return Response({'msg': _('Quantity requested is more than stock')}, status.HTTP_400_BAD_REQUEST)
            request.session.clear()

            return Response({'msg': _('The cart has been saved successfully')})
        except:
            return Response({'msg': _('error')})


class ShowOrdersView(GenericAPIView):
    serializer_class = ShowOrdersPostSerializers
    queryset = Cart.objects.all()

    def post(self, request: Request):
        translate(request)
        try:
            carts = Cart.objects.filter(user=request.data['user_id']).order_by('-created_at')
            all_item = []
            for cart in carts:
                items = CartItem.objects.filter(cart_id=cart.id)
                foods = []
                total_price = 0
                for item in items:
                    foods.append({
                        'food_name': item.food.name,
                        'food_image': '/media/' + str(item.food.image),
                        'food_category': item.food.category.title,
                        'food_price': item.price,
                        'quantity': item.quantity,
                        'final_price': item.total_price,
                    })
                    total_price += item.total_price
                all_item.append({
                    'cart': cart.id,
                    'user': {
                        'id': cart.user.id,
                        'phone_number': cart.user.phone_number
                    },
                    'foods': foods,
                    'total_price': total_price,
                    'status': cart.status.status,
                    'created_at': cart.created_at
                })

            return Response(all_item, status.HTTP_200_OK)
        except:
            return Response({'msg': _('error')}, status.HTTP_400_BAD_REQUEST)


class ShowAllOrdersAdminView(GenericAPIView):
    serializer_class = ShowOrdersSerializers
    queryset = Cart.objects.all().order_by('-created_at')

    def get(self, request: Request):
        translate(request)
        try:
            carts = Cart.objects.all().order_by('-created_at')
            all_items = []
            for cart in carts:
                items = CartItem.objects.filter(cart_id=cart.id)
                foods = []
                total_price = 0
                for item in items:
                    foods.append({
                        'food_name': item.food.name,
                        'food_image': '/media/' + str(item.food.image),
                        'food_category': item.food.category.title,
                        'food_price': item.price,
                        'quantity': item.quantity,
                        'final_price': item.total_price,
                    })
                    total_price += item.total_price
                all_items.append({
                    'cart': cart.id,
                    'user': {
                        'id': cart.user.id,
                        'phone_number': cart.user.phone_number
                    },
                    'foods': foods,
                    'total_price': total_price,
                    'status': cart.status.status,
                    'created_at': cart.created_at
                })

            return Response(all_items, status.HTTP_200_OK)
        except:
            return Response({'msg': _('error')}, status.HTTP_400_BAD_REQUEST)
