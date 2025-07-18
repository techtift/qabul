from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes

from university.services.questions.get_questions_by_faculty import get_questions_by_faculty


class GetQuestionsByFacultyResponseSerializer(serializers.Serializer):
    class SubQuestionSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        question_text = serializers.CharField()
        version_a = serializers.CharField(allow_blank=True, allow_null=True)
        version_b = serializers.CharField(allow_blank=True, allow_null=True)
        version_c = serializers.CharField(allow_blank=True, allow_null=True)
        version_d = serializers.CharField(allow_blank=True, allow_null=True)

    subject_id = serializers.IntegerField()
    subject_name = serializers.CharField()
    questions = SubQuestionSerializer(many=True)

class GetQuestionsByFacultyAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get Questions by Faculty",
        manual_parameters=[
            openapi.Parameter(
                name="total_questions",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False,
                description="Total number of questions to retrieve per faculty (default is 20)"
            ),
        ],
        responses={status.HTTP_200_OK: GetQuestionsByFacultyResponseSerializer(many=True)},
        tags=["Questions"]
    )
    def get(self, request):
        if 'lang' in request.query_params:
            lang = request.query_params.get('lang')
            if lang not in ['uz', 'ru']:
                raise CustomApiException(ErrorCodes.VALIDATION_FAILED, "Invalid language code")
            


        questions = get_questions_by_faculty(user_id=request.user.id)
        return Response(questions, status=status.HTTP_200_OK)

