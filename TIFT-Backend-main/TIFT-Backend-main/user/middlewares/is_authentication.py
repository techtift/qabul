from rest_framework import status
from django.urls import reverse
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from user.services.check_token import validate_token


class UserIsAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        allowed_urls = (
            reverse('create_otp'),
            reverse('create_user'),
            reverse('user_login'),
            reverse('reset_password_request'),
            reverse('verify_reset_code'),
            reverse('reset_password_confirm'),
            reverse('generate_contract'),
            reverse('generate_certificate'),
            reverse('student-registration'),
            # '/api/v1/auth/user/registration/',  # add your registration API explicitly

            # Admin url
            reverse('student-program-id'),
            reverse('student-get'),
            reverse('student-create-admin'),
            reverse('student-create-passport'),
            reverse('student-update'),
            reverse('create-student-application-admin')
        )
        allowed_path_urls = ('/admin/', '/swagger/',)
        if request.path.startswith(allowed_path_urls) or request.path in allowed_urls:
            return self.get_response(request)

        if request.path.startswith('/api/v1/'):
            payload = validate_token(request.headers.get('Authorization'))
            if payload is None:
                return JsonResponse(data={'result': '', 'error': 'UnAuthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return None