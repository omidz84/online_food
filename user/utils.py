from rest_framework_simplejwt.tokens import RefreshToken
import random


def get_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        "Refresh": str(refresh),
        "Access": str(refresh.access_token)
    }


def code(length: int=5) -> str:
    char = "0123456789"
    ret = ""
    for i in range(length):
        rand = random.choice(char)
        # print(rand)
        ret += rand

    return ret


