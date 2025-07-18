from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes

from university.services.questions.check_exam_valid_date import check_exam_valid_date

class CheckExamValidDateResponseSerializer(serializers.Serializer):
    is_valid = serializers.BooleanField(help_text="Indicates if the exam date is valid for the user")

class CheckExamValidDateAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Check Exam Valid Date",
        operation_description="Returns whether the current time falls within the student's application start/end dates.",
        manual_parameters=[
            openapi.Parameter(
                name="student_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="ID of the student to check exam validity for"
            )
        ],
        responses={status.HTTP_200_OK: CheckExamValidDateResponseSerializer()},
        tags=["Questions"]
    )
    def post(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            raise CustomApiException(
                ErrorCodes.INVALID_INPUT,
                "student_id is required"
            )

        is_valid = check_exam_valid_date(int(student_id))
        return Response({"is_valid": is_valid}, status=status.HTTP_200_OK)
