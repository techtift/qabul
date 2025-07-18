from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from university.services.generate_contract.generate_contract import generate_student_contract, generate_student_certificate


class GenerateContractAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="Generate Student Contract PDF",
        manual_parameters=[
            openapi.Parameter(
                name="student_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="ID of the student to generate contract for"
            ),
            openapi.Parameter(
                name="language",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description="Language for the contract, defaults to 'en'"
            ),
        ],
        tags=["Contracts"]
    )
    def get(self, request):
        student_id = request.query_params.get("student_id")
        language = request.query_params.get("language", "ru")
        if not student_id:
            return Response({"detail": "student_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        pdf_response = generate_student_contract(student_id, language)
        return pdf_response  # Already HttpResponse with PDF content

class GenerateCertificateAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Generate Student Certificate PDF",
        manual_parameters=[
            openapi.Parameter(
                name="student_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="ID of the student to generate certificate for"
            ),
            openapi.Parameter(
                name="language",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description="Language for the certificate, defaults to 'uz'"
            ),
        ],
        tags=["Certificates"]
    )
    def get(self, request):
        student_id = request.query_params.get("student_id")
        language = request.query_params.get("language", "uz")
        if not student_id:
            return Response({"detail": "student_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        pdf_response = generate_student_certificate(student_id, language)
        return pdf_response  # Already HttpResponse with PDF content