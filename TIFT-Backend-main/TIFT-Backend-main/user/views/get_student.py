from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from user.models.user import User
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from user.models.student import QUALIFICATION_CHOICES, Student, GENDER_CHOICES


class StudentResponseSerializer(serializers.Serializer):
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
    is_exam_exempt = serializers.BooleanField(required=False, default=False)
    is_passed_exam = serializers.BooleanField(required=False, default=False)
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


class GetStudentAPIView(APIView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: StudentResponseSerializer()},
        tags=["Student"],
    )
    def get(self, request):
        student = Student.objects.filter(user_id=request.user.id).first()
        if not student:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Student not found.')

        serializer = StudentResponseSerializer(student, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StudentListAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='User List API',
        operation_description='User List API',
        manual_parameters=[
            openapi.Parameter(
                name='is_registred', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description='Is Registred', required=False),
        ],
        responses={200: StudentResponseSerializer(many=True)},
        tags=["Student"],
    )
    def get(self, request):
        filter_ = {}
        is_registred = request.query_params.get('is_registred')
        if is_registred:
            filter_['is_registred'] = is_registred.lower() == 'true'

        students = Student.objects.filter(**filter_).order_by('-created_datetime')
        serializer = StudentResponseSerializer(students, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StudentDetailAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='User Detail API',
        operation_description='User Detail API',
        responses={200: StudentResponseSerializer()},
        tags=["Student"],
    )
    def get(self, request, pk):
        student = Student.objects.filter(id=pk).first()
        if not student:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='User not found.')
        serializer = StudentResponseSerializer(student)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
