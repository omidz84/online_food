from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import AccessToken

from user.models import MyUser


class IsAdmin(BasePermission):

    def has_permission(self, request: Request, view):
        try:
            user_jwt = request.META.get('HTTP_AUTHORIZATION')
            if user_jwt is not None:
                decoded_token = AccessToken(user_jwt)
                user = MyUser.objects.get(id=decoded_token["user_id"])
                return bool(user.type_id == 1)
            else:
                return False
        except:
            return False


# -----------------------------------------------------------------------


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request: Request, view):
        try:
            user_jwt = request.META.get('HTTP_AUTHORIZATION')
            if user_jwt is not None:
                decoded_token = AccessToken(user_jwt)
                user = MyUser.objects.get(id=decoded_token["user_id"])
                return bool(user.type_id == 1)
            elif request.method in SAFE_METHODS:
                return True
            else:
                return False
        except:
            return False


# -----------------------------------------------------------------------


class IsAdminOrDelivery(BasePermission):

    def has_permission(self, request: Request, view):
        try:
            user_jwt = request.META.get('HTTP_AUTHORIZATION')
            if user_jwt is not None:
                decoded_token = AccessToken(user_jwt)
                user = MyUser.objects.get(id=decoded_token["user_id"])
                return bool(user.type_id == 1 or user.type_id == 2)
            else:
                return False
        except:
            return False


# -----------------------------------------------------------------------


class IsAuthenticated(BasePermission):

    def has_permission(self, request: Request, view):
        try:
            user_jwt = request.META.get('HTTP_AUTHORIZATION')
            if user_jwt is not None:
                decoded_token = AccessToken(user_jwt)
                user = MyUser.objects.get(id=decoded_token["user_id"])
                return bool(user)
            else:
                return False
        except:
            return False
