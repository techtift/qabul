from django.contrib.auth.hashers import make_password
from user.models.user import User
from user.models.sms import OTP
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

def create_user_service(data):
    phone_number = data.get('phone_number')
    password = data.get('password')
    source = data.get('source', "web")

    opt = OTP.objects.filter(phone_number=phone_number).first()
    if not opt:
        raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)
    if not opt.is_verified:
        raise CustomApiException(ErrorCodes.NOT_VERIFIED)
    
    if User.objects.filter(phone_number=phone_number).exists():
        raise CustomApiException(ErrorCodes.ALREADY_EXISTS, message="User with this phone number already exists.")
    user = User(
        phone_number=phone_number,
        password=make_password(password),
        source=source,
        is_verified=True,
    )
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



