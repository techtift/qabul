from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from rest_framework import serializers

from user.services.reset_password import (
    reset_password_service,
    verify_reset_code_service,
    reset_password_confirm_service,
)


class ResetPasswordRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=15)


class VerifyResetCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=15)
    code = serializers.CharField(required=True, max_length=6)


class ResetPasswordConfirmSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=15)
    new_password = serializers.CharField(required=True, min_length=6)


class ResetPasswordRequestAPIView(APIView):
    @swagger_auto_schema(
        request_body=ResetPasswordRequestSerializer,
        tags=["reset"],
        operation_description="Send SMS code to verified user",
    )
    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        sms = reset_password_service(phone_number)
        return Response({"message": "Tasdiqlash kodi yuborildi.", "sms_id": sms.id}, status=status.HTTP_200_OK)


class VerifyResetCodeAPIView(APIView):
    @swagger_auto_schema(
        request_body=VerifyResetCodeSerializer,
        tags=["reset"],
        operation_description="Verify reset code sent to user",
    )
    def post(self, request):
        serializer = VerifyResetCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']
        verify_reset_code_service(phone_number, code)
        return Response({"message": "Kod tasdiqlandi."}, status=status.HTTP_200_OK)


class ResetPasswordConfirmAPIView(APIView):
    @swagger_auto_schema(
        request_body=ResetPasswordConfirmSerializer,
        tags=["reset"],
        operation_description="Confirm new password after code verification",
    )
    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        new_password = serializer.validated_data['new_password']
        reset_password_confirm_service(phone_number, new_password)
        return Response({"message": "Parol muvaffaqiyatli yangilandi."}, status=status.HTTP_200_OK)