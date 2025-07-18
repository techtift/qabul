from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from django.conf import settings
import os
from django.http import FileResponse, Http404

class BuildFileUrlRequestSerializer(serializers.Serializer):
    file_path = serializers.CharField(required=True, help_text="The path of the file to build the URL for.")

class BuildFileUrlResponseSerializer(serializers.Serializer):
    file_url = serializers.URLField(help_text="The full URL of the file.")

class BuildFileUrlAPIView(APIView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: BuildFileUrlResponseSerializer()},
        manual_parameters=[
            openapi.Parameter(
                name='path',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The path of the file to build the URL for."
            )
        ],
        tags=["File"]
    )
    def get(self, request):
        file_path = request.query_params.get('path')
        abs_path = os.path.join(settings.MEDIA_ROOT, file_path)
        print(f"\n\n Absolute path: {abs_path} \n\n")
        if not os.path.exists(abs_path):
            raise Http404("File not found")
        return FileResponse(open(abs_path, 'rb'))