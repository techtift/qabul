from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,parsers
from drf_yasg.utils import swagger_auto_schema
from user.models.student import Student
from university.services.student_dtm.create_student_dtm import create_student_dtm
from core.exceptions.error_messages import ErrorCodes
from core.exceptions.exception import CustomApiException

class StudentDtmRequestSerializer(serializers.Serializer):
    dtm_file = serializers.FileField(
        required=False,
        allow_empty_file=True,
        help_text="DTM blank fayli"
    )


class StudentDtmAPIView(APIView):
    
    parser_classes = [parsers.MultiPartParser]
    @swagger_auto_schema(
        request_body=StudentDtmRequestSerializer,
        responses={
            200: "DTM blank fayli muvaffaqiyatli yaratildi.",
            400: "Yaroqsiz so'rov ma'lumotlari."
        }
    )
    def post(self, request):
        
        student=Student.objects.filter(user_id=request.user.id).first()
        if not student:
            raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST,
                                 "The student with the provided ID does not exist.")
        serializer = StudentDtmRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            create_student_dtm(student=student,data=data)
            return Response(
                {"message": "DTM blank fayli muvaffaqiyatli yaratildi."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
