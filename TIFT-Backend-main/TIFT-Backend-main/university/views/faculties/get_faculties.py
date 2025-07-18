from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from django.utils import translation

from university.services.faculties.get_faculties import get_faculties

class FacultyResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name_uz = serializers.CharField(max_length=255)
    name_ru = serializers.CharField(max_length=255)
    program_id = serializers.IntegerField()
    program_name_uz = serializers.CharField(max_length=255)
    program_name_ru = serializers.CharField(max_length=255)

class GetFacultiesAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get All Faculties",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of faculties",
                schema=FacultyResponseSerializer(many=True)
            ),
        },
        manual_parameters=[
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
            faculties = get_faculties()
            serializer = FacultyResponseSerializer(faculties, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomApiException as e:
            return Response({"error": str(e)}, status=e.status_code)
