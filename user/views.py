from django.utils.translation import gettext as _
from rest_framework.generics import GenericAPIView

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from core.utils import translate
from online_food.settings import REDIS_JWT_TOKEN, REDIS_REFRESH_TIME, REDIS_CODE, REDIS_CODE_TIME
from .utils import get_tokens, code
from .models import MyUser, UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserCodeSerializer, UserCreateRefreshSerializer, \
                         UserLogoutSerializer, AddressSerializers

# Create your views here.

# ------------------------------------------------------------------------------------------------
# API_1


class UserCodeAPIView(APIView):
    serializer_class = UserCodeSerializer

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        sent_code = code()
        data = {
            "code": sent_code,
            "Message": _("The code is sent to the mobile.")
        }
        REDIS_CODE.set(name=request.data['phone_number'], value=sent_code, ex=REDIS_CODE_TIME)
        return Response(data, status.HTTP_201_CREATED)


# -----------------------------------------------------------------------

# API_2
class UserAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        if (REDIS_CODE.get(request.data["phone_number"]) is not None) and \
           (request.data["code"] == REDIS_CODE.get(request.data["phone_number"]).decode('utf-8')):
            try:
                user = MyUser.objects.get(phone_number=request.data["phone_number"])
                tokens = get_tokens(user)
                access_token = tokens['Access']
                refresh_token = tokens['Refresh']
                REDIS_JWT_TOKEN.set(name=refresh_token, value=refresh_token, ex=REDIS_REFRESH_TIME)
                data = {
                    "user": {
                        "phone_number": user.phone_number,
                        "type": user.type
                    },
                    "AccessToken": access_token,
                    "RefreshToken": REDIS_JWT_TOKEN.get(refresh_token),
                    "Message": _("You are login successfully")
                }
                return Response(data, status.HTTP_200_OK)

            except MyUser.DoesNotExist:
                user = MyUser.objects.create(phone_number=request.data['phone_number'])
                tokens = get_tokens(user)
                access_token = tokens['Access']
                refresh_token = tokens['Refresh']
                REDIS_JWT_TOKEN.set(name=refresh_token, value=refresh_token, ex=REDIS_REFRESH_TIME)
                data = {
                    "user": {
                        "phone_number": user.phone_number,
                        "type": user.type
                    },
                    "Access Token": access_token,
                    "Refresh Token": REDIS_JWT_TOKEN.get(refresh_token),
                    "Message": _("You are registered successfully")
                }
                return Response(data, status.HTTP_201_CREATED)
        else:
            return Response({"Message": _("The code is not valid")})

# -------------


class UserCreateRefreshAPIView(APIView):
    serializer_class = UserCreateRefreshSerializer

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)

        try:
            token = request.data["refresh_token"]
            REDIS_JWT_TOKEN.delete(token)
            decoded_token = RefreshToken(token)
            user = MyUser.objects.get(id=decoded_token["user_id"])
            access_refresh_token = get_tokens(user)
            access_token = access_refresh_token["Access"]
            REDIS_JWT_TOKEN.set(name=token, value=token, ex=REDIS_REFRESH_TIME)
            data = {
                "Access Token": access_token,
                "Refresh Token": token
            }
            return Response(data, status.HTTP_201_CREATED)
        except:
            return Response({"Message": _("Token is Expired")})


# -----------------------------------------------------------------------

# API_3


class UserProfileAPIView(APIView):
    serializer_class = UserProfileSerializer
    lookup_field = "slug"

    # def get(self, request: Request, slug) -> Response:
    #     user = UserProfile.objects.get(slug=slug)
    #     return Response({user.first_name})

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Message": _("Your Profile is Complete.")})



# class UserProfileDetailAPIView(APIView):
#     serializer_class = UserProfileSerializer
#
#     def get(self, request: Request, slug):
#         try:
#             user = UserProfile.objects.get(full_name=request.data["full_name"])

# -----------------------------------------------------------------------

# API_4


class UserLogoutAPIView(APIView):
    serializer_class = UserLogoutSerializer

    def post(self, request: Request) -> Response:
        translate(request)
        serializer = self.serializer_class(data=request.data)
        refresh_token = request.data["refresh_token"]
        try:
            REDIS_JWT_TOKEN.get(refresh_token)
            REDIS_JWT_TOKEN.delete(refresh_token)
            return Response({"Message": _("You Are Logged Out Successfully")})
        except Exception:
            return Response({"Message": _("There is No Refresh Token in Redis")})


# ----------------------------------------------------------------------------------

class AddressView(GenericAPIView):
    serializer_class = AddressSerializers

    def post(self, request):
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
