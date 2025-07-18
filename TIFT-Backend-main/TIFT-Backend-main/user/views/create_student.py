from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import serializers
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from drf_yasg.utils import swagger_auto_schema
from user.services.student_create import student_create_service
from rest_framework.parsers import MultiPartParser, FormParser

class CreateStudentRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    last_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    father_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    additional_phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    birth_date = serializers.DateField(required=True, allow_null=False)
    birth_place = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    citizenship = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    passport_number = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    qualification = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    name_qualification = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    diploma = serializers.FileField(required=False, allow_empty_file=True, allow_null=True)
    photo = serializers.ImageField(required=False, allow_empty_file=True, allow_null=True)

class CreateStudentResponseSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()

class CreateStudentAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=CreateStudentRequestSerializer,
        consumes=['multipart/form-data'],  # <-- This makes file/image inputs appear!
        responses={status.HTTP_201_CREATED: CreateStudentResponseSerializer()},
        tags=["user"],
    )
    def post(self, request):
        serializer = CreateStudentRequestSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, serializer.errors)

        # Suppose you POST user_id in request.data, or you get it from request.user
        user_id = request.user.id 
        if not user_id:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, "User ID required.")

        student_data = serializer.validated_data
        student = student_create_service(user_id, student_data)

        response_serializer = CreateStudentResponseSerializer({"student_id": student.id})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)