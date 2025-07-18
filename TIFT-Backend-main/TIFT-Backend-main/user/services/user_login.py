from django.utils import timezone
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from user.models.user import User
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes


def user_login_service(data):
    phone_number = data.get('phone_number')
    password = data.get('password')

    user = User.objects.filter(phone_number=phone_number).first()
    if not user:
        raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)
       
    if not user.is_verified:
        raise CustomApiException(ErrorCodes.NOT_VERIFIED)

    if not check_password(password, user.password):
        raise CustomApiException(ErrorCodes.INCORRECT_PASSWORD)

    user.last_login = timezone.now()
    user.save()

    refresh = RefreshToken.for_user(user)
    # Add custom fields if needed:
    refresh['user_id'] = user.id
    refresh['login_time'] = str(user.last_login)

    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }
