from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from django.utils import translation

from university.services.applications.get_applications import get_applications

class GetApplicationsResponseSerializer(serializers.Serializer):
    class ApplicationsProgramSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name_uz = serializers.CharField()
        name_ru = serializers.CharField()

    class ApplicationsFacultySerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name_uz = serializers.CharField()
        name_ru = serializers.CharField()
        program_id = serializers.IntegerField(source='program.id')
        program_name_uz = serializers.CharField(source='program.name_uz')
        program_name_ru = serializers.CharField(source='program.name_ru')
    class ApplicationStudyTypeSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name_uz = serializers.CharField()
        name_ru = serializers.CharField()
        description_uz = serializers.CharField(allow_null=True)
        description_ru = serializers.CharField(allow_null=True)
    
    class ApplicationsExamsSerializer(serializers.Serializer):
        program_id = serializers.IntegerField(source='program.id')
        program_name_uz = serializers.CharField(source='program.name_uz')
        program_name_ru = serializers.CharField(source='program.name_ru')
        faculty_id = serializers.IntegerField(source='faculty.id')
        faculty_code = serializers.CharField(source='faculty.code')
        faculty_day_price = serializers.FloatField(source='faculty.price', allow_null=True)
        faculty_night_price = serializers.FloatField(source='faculty.night_price', allow_null=True)
        faculty_external_price = serializers.FloatField(source='faculty.external_price', allow_null=True)
        faculty_name_uz = serializers.CharField(source='faculty.name_uz')
        faculty_name_ru = serializers.CharField(source='faculty.name_ru')
        is_online = serializers.BooleanField()
        exam_date = serializers.DateTimeField(allow_null=True)

    class ApplicationExamTypeSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name_uz = serializers.CharField()
        name_ru = serializers.CharField()
        description_uz = serializers.CharField(allow_null=True)
        description_ru = serializers.CharField(allow_null=True)

    id = serializers.IntegerField()
    title_uz = serializers.CharField()
    title_ru = serializers.CharField()
    description_uz = serializers.CharField(allow_null=True)
    description_ru = serializers.CharField(allow_null=True)
    programs = ApplicationsProgramSerializer(many=True)
    faculties = ApplicationsFacultySerializer(many=True)
    study_types = ApplicationStudyTypeSerializer(many=True)
    exams = ApplicationsExamsSerializer(many=True)
    exam_types = ApplicationExamTypeSerializer(many=True)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    created_datetime = serializers.DateTimeField(allow_null=True)

class GetApplicationsAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get Applications",
        manual_parameters=[
            openapi.Parameter(
                name="only_valid",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="Filter only valid applications",
                required=False,
                default=True
            ),
            openapi.Parameter(
                name="application_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Filter by application ID",
                required=False
            ),
            openapi.Parameter(
                name="lang",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Language for translations, e.g., 'uz', 'ru'",
                required=False
            ),
        ],
        responses={
            status.HTTP_200_OK: GetApplicationsResponseSerializer(many=True)
        },
        tags=["Applications"],
    )
    def get(self, request):
        lang = request.query_params.get("lang")
        if lang:
            translation.activate(lang)
        only_valid = request.query_params.get('only_valid', 'true').lower() == 'true'
        application_id = request.query_params.get('application_id')


        applications = get_applications(only_valid=only_valid, application_id=application_id)
        serializer = GetApplicationsResponseSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
