from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import UserType
from cart.models import Status


def token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh)
    }


class Command(BaseCommand):
    help = 'create token refresh for anonymous user'

    def handle(self, *args, **options):

        user = User.objects.get_or_create(username='anonymous', password='anonymoususerfortoken')
        settings.REDIS_JWT_TOKEN.flushdb()
        token = token_for_user(user[0])
        refresh = token['refresh']
        settings.REDIS_JWT_TOKEN.set(refresh, refresh, settings.REDIS_REFRESH_TIME_CHECK_SYSTEM)

        # user type ------------------------------------------------------------------------------

        UserType.objects.get_or_create(title='ادمین')
        UserType.objects.get_or_create(title='پیک')
        UserType.objects.get_or_create(title='مشتری')

        # status ----------------------------------------------------------------------------------

        Status.objects.get_or_create(status='در حال آماده سازی')
        Status.objects.get_or_create(status='آماده شد')
        Status.objects.get_or_create(status='تحویل به پیک')
        Status.objects.get_or_create(status='تحویل به مشتری')



