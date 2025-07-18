from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import serializers
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from drf_yasg.utils import swagger_auto_schema
from user.services.user_login import user_login_service


class UserLoginRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserLoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    refresh_token = serializers.CharField(required=True)


class UserLoginAPIView(APIView):
    @swagger_auto_schema(
        request_body=UserLoginRequestSerializer,
        responses={status.HTTP_200_OK: UserLoginResponseSerializer()},
        tags=["user"],
    )
    def post(self, request):
        serializer = UserLoginRequestSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, serializer.errors)
        response = user_login_service(serializer.data)
        serializer = UserLoginResponseSerializer(response)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
