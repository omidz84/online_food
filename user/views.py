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

    def post(self, request: Request):
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        sent_code = code()
        data = {
            "code": sent_code,
            "Message": _("The code is sent to the mobile.")
        }
        REDIS_CODE.set(name=request.data['phoneNumber'], value=sent_code, ex=REDIS_CODE_TIME)
        return Response(data, status.HTTP_201_CREATED)


# -----------------------------------------------------------------------

# API_2
class UserAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, request: Request):
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if (REDIS_CODE.get(request.data["phoneNumber"]) is not None) and (request.data["code"] == REDIS_CODE.get(request.data["phoneNumber"]).decode('utf-8')):
            try:
                user = MyUser.objects.get(phoneNumber=request.data["phoneNumber"])
                tokens = get_tokens(user)
                access_token = tokens['Access']
                refresh_token = tokens['Refresh']
                REDIS_JWT_TOKEN.set(name=refresh_token, value=refresh_token, ex=REDIS_REFRESH_TIME)
                data = {
                    "user": {
                        "phoneNumber": user.phoneNumber,
                            "type": user.type
                    },
                    "AccessToken": access_token,
                    "RefreshToken": REDIS_JWT_TOKEN.get(refresh_token),
                    "Message": _("You are logined successfully")
                }
                return Response(data, status.HTTP_200_OK)

            except MyUser.DoesNotExist:
                user = MyUser.objects.create(phoneNumber=request.data['phoneNumber'])
                tokens = get_tokens(user)
                access_token = tokens['Access']
                refresh_token = tokens['Refresh']
                REDIS_JWT_TOKEN.set(name=refresh_token, value=refresh_token, ex=REDIS_REFRESH_TIME)
                data = {
                    "user": {
                        "phoneNumber": user.phoneNumber,
                        "type": user.type
                    },
                    "AccessToken": access_token,
                    "RefreshToken": REDIS_JWT_TOKEN.get(refresh_token),
                    "Message": _("You are registered successfully")
                }
                return Response(data, status.HTTP_201_CREATED)
        else:
            return Response({"Message": _("The code is not valid")})

# -------------


class UserCreateRefreshAPIView(APIView):
    serializer_class = UserCreateRefreshSerializer

    def post(self, request: Request):
        translate(request)
        serializer = self.serializer_class(data=request.data)

        try:
            token = request.data["refreshToken"]
            REDIS_JWT_TOKEN.delete(token)
            decodedToken = RefreshToken(token)
            user = MyUser.objects.get(id=decodedToken["user_id"])
            accessRefreshToken = get_tokens(user)
            print(accessRefreshToken)
            accessToken = accessRefreshToken["Access"]
            REDIS_JWT_TOKEN.set(name=token, value=token, ex=REDIS_REFRESH_TIME)
            return Response({"New Access Token": accessToken}, status.HTTP_201_CREATED)
        except MyUser.DoesNotExist:
            return Response({"Message": _("Token is Expired")})


# -----------------------------------------------------------------------

# API_3


class UserProfileAPIView(APIView):
    serializer_class = UserProfileSerializer

    def post(self, request: Request):
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Message": _("Your Profile is Complete.")})

# -----------------------------------------------------------------------

# API_4


class UserLogoutAPIView(APIView):
    serializer_class = UserLogoutSerializer

    def post(self, request: Request):
        translate(request)
        serializer = self.serializer_class(data=request.data)
        refreshToken = request.data["refreshToken"]
        try:
            REDIS_JWT_TOKEN.get(refreshToken)
            REDIS_JWT_TOKEN.delete(refreshToken)
            return Response({"Message": _("You Are Logged Out Successfully")})
        except Exception:
            return Response({"Message": _("There is No Refresh Token in Redis")})


class AddressView(GenericAPIView):
    serializer_class = AddressSerializers

    def post(self, request):
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
