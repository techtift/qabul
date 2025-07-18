from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from user.models.user import User
from user.services.create_user import create_user_service
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from user.models.student import QUALIFICATION_CHOICES

class CreateUserRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    source = serializers.CharField(required=False, allow_blank=True, allow_null=True, default="web")


class UserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    uuid = serializers.UUIDField(required=False, allow_null=True)
    phone_number = serializers.CharField()

class UserTokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    refresh_token = serializers.CharField(required=True)

class CreateUserAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='Create Student API',
        operation_description='Create Student API',
        request_body=CreateUserRequestSerializer,
        responses={status.HTTP_201_CREATED: UserTokenResponseSerializer()},
        tags=["user"],
    )
    def post(self, request):
        serializer = CreateUserRequestSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        data = serializer.validated_data
        user = create_user_service(data)

        response_serializer = UserTokenResponseSerializer(instance=user)
        return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)

class UserMeAPIView(APIView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: UserResponseSerializer()},
        tags=["user"],
    )
    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            raise CustomApiException(ErrorCodes.UNAUTHORIZED, message='User not found.')

        serializer = UserResponseSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserListAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='User List API',
        operation_description='User List API',
        manual_parameters=[
            openapi.Parameter(
                name='is_verified', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description='Is verified', required=False),
        ],
        responses={200: UserResponseSerializer()},
        tags=["user"],
    )
    def get(self, request):
        filter_ = {}

        is_verified = request.query_params.get('is_verified')
        if is_verified:
            filter_['is_verified'] = is_verified.lower() == 'true'

        users = User.objects.filter(**filter_).order_by('-created_datetime').exclude(id=request.user.id)
        serializer = UserResponseSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserDetailAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='User Detail API',
        operation_description='User Detail API',
        responses={200: UserResponseSerializer()},
        tags=["user"],
    )
    def get(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='User not found.')
        serializer = UserResponseSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
