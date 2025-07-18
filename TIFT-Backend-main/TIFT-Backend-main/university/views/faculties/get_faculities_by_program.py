from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from django.utils import translation

from university.services.faculties.get_faculities_by_program import get_faculties_by_program

class GetFacultiesByProgramResponseSerializer(serializers.Serializer):
    class SubFacultySerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name_uz = serializers.CharField(max_length=255)
        name_ru = serializers.CharField(max_length=255)
    id = serializers.IntegerField()
    name_uz = serializers.CharField(max_length=255)
    name_ru = serializers.CharField(max_length=255)
    faculties = SubFacultySerializer(many=True)

# --- API View ---
class GetFacultiesByProgramAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get All Faculties By Program",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of faculties by program",
                schema=GetFacultiesByProgramResponseSerializer(many=True)
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                name="program_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False,
                description="ID of the program to filter faculties by"
            ),
            openapi.Parameter(
                name="lang",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description="Language code for the response (e.g., 'uz', 'ru')"
            ),
        ],
        tags=["Faculties"],
    )
    def get(self, request):
        try:
            lang = request.query_params.get("lang")
            if lang:
                translation.activate(lang)
            program_id = request.query_params.get('program_id')
            faculties = get_faculties_by_program(program_id)
            serializer = GetFacultiesByProgramResponseSerializer(faculties, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomApiException as e:
            return Response({"error": str(e)}, status=e.status_code)