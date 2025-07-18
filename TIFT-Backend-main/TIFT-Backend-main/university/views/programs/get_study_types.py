from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from django.utils import translation
from university.services.programs.get_study_types import get_study_types


class ProgramStudyTypeResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name_uz = serializers.CharField(max_length=255)
    name_ru = serializers.CharField(max_length=255)
    description_uz = serializers.CharField(max_length=500, allow_blank=True, allow_null=True)
    description_ru = serializers.CharField(max_length=500, allow_blank=True, allow_null=True)

class GetProgramsStudyTypesAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get All Programs",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of programs",
                schema=ProgramStudyTypeResponseSerializer(many=True)
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                name="lang",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description="Language code for the response (e.g., 'uz', 'ru')"
            ),openapi.Parameter(
                name="program_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description="Program ID to filter study types by"
            ),
        ],
        tags=["Programs"],
    )
    def get(self, request):
        try:
            program_id = request.query_params.get('program_id')
            lang = request.query_params.get("lang")
            if lang:
                translation.activate(lang)
            if not program_id:
                return Response({"error": "Program ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            study_types = get_study_types(program_id=program_id)
            serializer = ProgramStudyTypeResponseSerializer(study_types, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomApiException as e:
            return Response({"error": str(e)}, status=e.status_code)
