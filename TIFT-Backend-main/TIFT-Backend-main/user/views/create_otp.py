from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import serializers
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from drf_yasg.utils import swagger_auto_schema
from user.services.create_otp import create_otp_service, verify_otp

class CreateOTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    code = serializers.CharField(required=False)

class CreateOTPResponseSerializer(serializers.Serializer):
    is_sent = serializers.BooleanField()

class CreateOTPAPIView(APIView):
    @swagger_auto_schema(
        request_body=CreateOTPRequestSerializer,
        responses={status.HTTP_200_OK: CreateOTPResponseSerializer()},
        tags=["user"],
    )
    def post(self, request):
        serializer = CreateOTPRequestSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, serializer.errors)

        phone_number = serializer.validated_data.get('phone_number')
        code = serializer.validated_data.get('code')

        if code:
            if verify_otp(phone_number, code):
                return Response({"is_verified": True}, status=status.HTTP_200_OK)
            else:
                raise CustomApiException(ErrorCodes.EXPIRED_OTP, "OTP expired or incorrect.")

        response = create_otp_service(phone_number)
        return Response({"is_sent": True}, status=status.HTTP_200_OK)