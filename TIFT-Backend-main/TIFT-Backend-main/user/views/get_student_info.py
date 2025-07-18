from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from user.models.user import User
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from user.services.get_student_info import get_student_info_service

class GetStudentInfoRequestSerializer(serializers.Serializer):
    pinfl = serializers.CharField(required=True, allow_blank=False, allow_null=False)

class GetStudentInfoResponseSerializer(serializers.Serializer):
    data = serializers.DictField(required=True)

class GetStudentInfoAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='Get Student Info API',
        operation_description='Get Student Info API',
        request_body=GetStudentInfoRequestSerializer,
        responses={status.HTTP_200_OK: GetStudentInfoResponseSerializer()},
        tags=["Student"],
    )
    def post(self, request):
        serializer = GetStudentInfoRequestSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        
        pinfl = serializer.validated_data.get('pinfl')
        
        student_info = get_student_info_service(pinfl)
        
        return Response({"data": student_info}, status=status.HTTP_200_OK)
