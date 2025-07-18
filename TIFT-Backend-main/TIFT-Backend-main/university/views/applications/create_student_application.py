from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser

from university.services.applications.create_student_application import create_student_application


class CreateStudentApplicationRequestSerializer(serializers.Serializer):
    application_id = serializers.IntegerField()
    program_id = serializers.IntegerField(required=False, allow_null=True)
    faculty_id = serializers.IntegerField(required=False, allow_null=True)
    is_transfer = serializers.BooleanField(required=True)
    transfer_level = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    study_type_id = serializers.IntegerField(required=False, allow_null=True)
    is_online_exam = serializers.BooleanField(default=True)
    exam_date_id = serializers.IntegerField(required=False, allow_null=True)
    transcript = serializers.FileField(required=False, allow_null=True)
    lang = serializers.CharField(default='uz', allow_blank=True, allow_null=True)

class CreateStudentApplicationResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class CreateStudentApplicationAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_summary="Create Student Application",
        request_body=CreateStudentApplicationRequestSerializer,
        consumes=['multipart/form-data'],
        responses={
            status.HTTP_201_CREATED: CreateStudentApplicationResponseSerializer()
        },
        tags=["Applications"]
    )
    def post(self, request):
        serializer = CreateStudentApplicationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application_data = serializer.validated_data
        student_app = create_student_application(application_data, user_id=request.user.id)
        response_serializer = CreateStudentApplicationResponseSerializer(student_app)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
