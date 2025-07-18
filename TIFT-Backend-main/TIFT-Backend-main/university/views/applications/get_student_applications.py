from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from django.utils import translation

from university.services.applications.get_student_applications import get_student_applications

class StudentApplicationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(source='student.first_name')
    last_name = serializers.CharField(source='student.last_name')
    father_name = serializers.CharField(source='student.father_name')
    birth_date = serializers.DateField(source='student.birth_date')
    passport_number = serializers.CharField(source='student.passport_number', allow_blank=True, allow_null=True)
    pinfl = serializers.CharField(source='student.pinfl', allow_blank=True, allow_null=True)
    application_id = serializers.IntegerField(source='application.id', allow_null=True)
    application_title = serializers.CharField(source='application.title', allow_blank=True, allow_null=True)
    program_id = serializers.IntegerField(source='program.id', allow_null=True)
    program_name_uz = serializers.CharField(source='program.name_uz', allow_blank=True, allow_null=True)
    program_name_ru = serializers.CharField(source='program.name_ru', allow_blank=True, allow_null=True)
    faculty_id = serializers.IntegerField(source='faculty.id', allow_null=True)
    faculty_code = serializers.CharField(source='faculty.code', allow_blank=True, allow_null=True)
    faculty_day_price = serializers.CharField(source='faculty.day_price', allow_null=True)
    faculty_night_price = serializers.CharField(source='faculty.night_price', allow_null=True)
    faculty_external_price = serializers.CharField(source='faculty.external_price', allow_null=True)
    faculty_name_uz = serializers.CharField(source='faculty.name_uz', allow_blank=True, allow_null=True)
    faculty_name_ru = serializers.CharField(source='faculty.name_ru', allow_blank=True, allow_null=True)
    is_transfer = serializers.BooleanField()
    score = serializers.FloatField(allow_null=True)
    is_online_exam = serializers.BooleanField()
    lang = serializers.CharField(allow_null=True)
    transfer_level = serializers.CharField(allow_blank=True, allow_null=True)
    study_type_id = serializers.IntegerField(source='study_type.id', allow_null=True)
    study_type_name = serializers.CharField(source='study_type.name', allow_blank=True, allow_null=True)
    exam_date_id = serializers.IntegerField(source='exam_date.id', allow_null=True)
    exam_date = serializers.DateTimeField(source='exam_date.exam_date', allow_null=True)
    created_datetime = serializers.DateTimeField()
    modified_datetime = serializers.DateTimeField()

class GetStudentApplicationsAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get Applications",
        manual_parameters=[
            openapi.Parameter(
                name="student_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False,
                description="ID of the user to filter applications by"
            ),
            openapi.Parameter(
                name="program_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False,
                description="ID of the program to filter applications by"
            ),
            openapi.Parameter(
                name="faculty_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False,
                description="ID of the faculty to filter applications by"
            ),
            openapi.Parameter(
                name="lang",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description="Language for translations (e.g., 'uz', 'ru')"
            )
        ],
        tags=["Applications"],
        responses={status.HTTP_200_OK: openapi.Response(
            description="List of applications",
            schema=StudentApplicationSerializer(many=True)
        )}
    )
    def get(self, request):
        try:
            lang = request.query_params.get("lang")
            if lang:
                translation.activate(lang)
            student_id = request.query_params.get("student_id")
            program_id = request.query_params.get("program_id")
            faculty_id = request.query_params.get("faculty_id")
            
            student_id = int(student_id) if student_id else None
            program_id = int(program_id) if program_id else None
            faculty_id = int(faculty_id) if faculty_id else None

            applications = get_student_applications(
                student_id=student_id,
                program_id=program_id,
                faculty_id=faculty_id
            )
            serializer = StudentApplicationSerializer(applications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomApiException as e:
            return Response({"error": str(e)}, status=e.status_code)
