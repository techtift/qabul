from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes

from university.services.questions.check_questions import check_questions

class CheckQuestionsRequestSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=True, help_text="ID of the question to check")
    selected = serializers.CharField(required=True, help_text="Selected answer for the question")

class CheckQuestionsResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField(help_text="Total number of questions")
    correct = serializers.IntegerField(help_text="Number of correctly answered questions")
    score_percent = serializers.FloatField(help_text="Percentage score based on correct answers")
    passed = serializers.BooleanField(help_text="Whether the student passed the exam (score >= 30%)")

class CheckQuestionsAPIView(APIView):
    @swagger_auto_schema(
        request_body=CheckQuestionsRequestSerializer(many=True),
        responses={status.HTTP_200_OK: CheckQuestionsResponseSerializer()},
        tags=["Questions"],
        operation_summary="Check Answers to Questions"
    )
    def post(self, request):
        serializer = CheckQuestionsRequestSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, serializer.errors)

        data = serializer.validated_data
        user_id = request.user.id

        result = check_questions(user_id, data)
        return Response(result, status=status.HTTP_200_OK)

