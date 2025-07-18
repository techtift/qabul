from django.contrib.auth.hashers import make_password
from core.exceptions.error_messages import ErrorCodes
from core.exceptions.exception import CustomApiException
from user.models.user import User


def create_user_admin(phone_number):
    user=User.objects.filter(phone_number=phone_number).first()
    if user:
        raise CustomApiException(ErrorCodes.ALREADY_EXISTS, message="Bu raqam bilan student mavjud")
    password = 'admin_password'
    source = "admin"
    user_created = User.objects.create(
        phone_number=phone_number,
        password=make_password(password),
        source=source,
        is_verified=True,
    )
    return user_created