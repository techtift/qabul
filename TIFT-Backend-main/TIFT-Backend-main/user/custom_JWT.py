from rest_framework_simplejwt.authentication import JWTAuthentication
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from user.models.user import User


class CustomJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_model = User

    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')

        if not user_id:
            raise CustomApiException(ErrorCodes.INVALID_TOKEN, message='Token missing user identification.')

        user = User.objects.filter(id=user_id, is_active=True).first()
        if not user:
            raise CustomApiException(ErrorCodes.UNAUTHORIZED, message='User does not exist or is blocked.')
        return user
