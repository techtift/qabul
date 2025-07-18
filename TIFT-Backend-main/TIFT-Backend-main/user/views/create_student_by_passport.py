from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import serializers
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from drf_yasg.utils import swagger_auto_schema
from user.services.create_student_by_passport import student_create_by_passport_service
from rest_framework.parsers import MultiPartParser, FormParser
from user.models.student import GENDER_CHOICES, QUALIFICATION_CHOICES
import datetime

class CreateStudentByPassportRequestSerializer(serializers.Serializer):
    birth_date = serializers.DateField(required=True, allow_null=False)
    passport_number = serializers.CharField(required=True, allow_blank=False, allow_null=False)

class CreateStudentByPassportResponseSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(source='user.id')
    user_uuid = serializers.UUIDField(source='user.uuid', required=False, allow_null=True)
    id = serializers.IntegerField()
    uuid = serializers.UUIDField(required=False, allow_null=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    father_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(source='user.phone_number', required=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    birth_place = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    citizenship = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    passport_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    pinfl = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=False, allow_null=True)
    is_registred = serializers.BooleanField(required=False, default=False)
    qualification = serializers.ChoiceField(choices=QUALIFICATION_CHOICES, required=False, allow_null=True)
    is_attended_exam = serializers.BooleanField(required=False, default=False)
    name_qualification = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    diploma = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    additional_phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def get_diploma(self, obj):
        # If diploma exists, return its full URL
        request = self.context.get('request')
        if obj.diploma and hasattr(obj.diploma, 'url'):
            if request is not None:
                return request.build_absolute_uri(obj.diploma.url)
            return obj.diploma.url
        return None

    def get_photo(self, obj):
        # If photo exists, return its full URL
        request = self.context.get('request')
        if obj.photo and hasattr(obj.photo, 'url'):
            if request is not None:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None
    
class CreateStudentByPassportAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=CreateStudentByPassportRequestSerializer,
        responses={status.HTTP_201_CREATED: CreateStudentByPassportResponseSerializer()},
        tags=["Student"],
    )
    def post(self, request):
        serializer = CreateStudentByPassportRequestSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, serializer.errors)

        birth_date_val = serializer.validated_data.get('birth_date')
        if isinstance(birth_date_val, (datetime.date, datetime.datetime)):
            birth_date_val = birth_date_val.isoformat()        
        passport_number = serializer.validated_data.get('passport_number')

        student = student_create_by_passport_service(birth_date_val, passport_number, request.user.id)

        response_serializer = CreateStudentByPassportResponseSerializer(student, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)