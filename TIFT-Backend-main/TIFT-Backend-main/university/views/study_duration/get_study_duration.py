from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from university.services.study_duration.get_study_duration import get_study_duration




class StudyDurationResponseSerializer(serializers.Serializer):
    study_duration = serializers.FloatField(required=False, allow_null=True)








class GetStudyDurationAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get Study Duration by Faculty and Study Type",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Study duration in years",
                schema=StudyDurationResponseSerializer()
            ),
            status.HTTP_400_BAD_REQUEST: "Invalid or missing parameters",
        },
        manual_parameters=[
            openapi.Parameter(
                name="faculty_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="Faculty ID"
            ),
            openapi.Parameter(
                name="study_type_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="Study Type ID"
            ),
        ],
        tags=["Study Duration"],
    )
    def get(self, request):
        faculty_id = request.query_params.get("faculty_id")
        study_type_id = request.query_params.get("study_type_id")

        if not faculty_id or not study_type_id:
            return Response(
                {"error": "faculty_id and study_type_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            faculty_id = int(faculty_id)
            study_type_id = int(study_type_id)
        except ValueError:
            return Response(
                {"error": "faculty_id and study_type_id must be integers"},
                status=status.HTTP_400_BAD_REQUEST
            )
        study_duration = get_study_duration(faculty_id, study_type_id)
        serializer = StudyDurationResponseSerializer({"study_duration": study_duration})
        return Response(serializer.data, status=status.HTTP_200_OK)