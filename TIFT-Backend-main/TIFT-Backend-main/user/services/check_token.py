from user.models.user import User
from .get_user_token import decode_jwt_token

def validate_token(token):
    if token is None:
        return
    if len(token.split()) < 2 or token.split()[0] != "Bearer":
        return
    if decode_jwt_token(token.split()[1]) is None:
        return
    user_id = decode_jwt_token(token.split()[1]).get('user_id', None)
    if user_id is None:
        return
    if User.objects.filter(id=user_id).exists():
        return decode_jwt_token(token.split()[1])
    return
