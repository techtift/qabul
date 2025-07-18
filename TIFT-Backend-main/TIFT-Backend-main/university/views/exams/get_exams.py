from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes

from university.services.exams.get_exams import get_exams_by_program_or_faculty

class GetExamsResponseSerializer(serializers.Serializer):
    class SubExamProgramSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField(max_length=255)
    class SubExamFacultySerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField(max_length=255)
    id = serializers.IntegerField()
    exam_type = serializers.CharField(required=False, allow_null=True)  # Change to match model field type
    exam_date = serializers.DateTimeField()
    is_online = serializers.BooleanField()
    program = SubExamProgramSerializer(required=False, allow_null=True)
    faculty = SubExamFacultySerializer(required=False, allow_null=True)

class GetExamsAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get All Exams By Program or Faculty",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of exams by program or faculty",
                schema=GetExamsResponseSerializer(many=True)
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                name="program_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False,
                description="ID of the program to filter exams by"
            ),
            openapi.Parameter(
                name="faculty_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False,
                description="ID of the faculty to filter exams by"
            ),
        ],
        tags=["Exams"],
    )
    def get(self, request):
        try:
            program_id = request.query_params.get('program_id')
            faculty_id = request.query_params.get('faculty_id')
            if program_id is not None:
                program_id = int(program_id)
            if faculty_id is not None:
                faculty_id = int(faculty_id)
            exams = get_exams_by_program_or_faculty(program_id, faculty_id)
            serializer = GetExamsResponseSerializer(exams, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomApiException as e:
            return Response({"error": str(e)}, status=e.status_code)