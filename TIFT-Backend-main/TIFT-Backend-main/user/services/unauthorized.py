from core.exceptions.error_messages import ErrorCodes
from core.exceptions.exception import CustomApiException
from user.models.user import User


def is_authenticated(request):
    if not User.objects.filter(id=request.user.id, is_blocked=False).exists():
        raise CustomApiException(ErrorCodes.UNAUTHORIZED)
