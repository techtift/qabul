from django.urls import path
from user.views.login import UserLoginAPIView
from user.views.user import (
    UserMeAPIView, UserDetailAPIView, UserListAPIView, CreateUserAPIView
)
from user.views.get_student import GetStudentAPIView, StudentListAPIView, StudentDetailAPIView
from user.views.create_otp import CreateOTPAPIView
from user.views.get_student_info import GetStudentInfoAPIView
from user.views.create_student import CreateStudentAPIView
from user.views.create_student_by_passport import CreateStudentByPassportAPIView
from user.views.update_student_info import UpdateStudentInfoAPIView
from user.views.reset_password import (
    ResetPasswordRequestAPIView, VerifyResetCodeAPIView, ResetPasswordConfirmAPIView
)
from user.admin_services.get_study_type import( student_registration_view, GetProgramIDView, GetStudentView,
    StudentCreateView, StudentCreateByPassportView, StudentUpdateView,CreateStudentApplication)

urlpatterns = [
    # User
    path('me/', UserMeAPIView.as_view(), name='user_me_apiview'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('create-user/', CreateUserAPIView.as_view(), name='create_user'),
    path('user-list/', UserListAPIView.as_view(), name='user_list'),
    path('user-detail/<int:pk>/', UserDetailAPIView.as_view(), name='user_detail'),

    #sms
    path('create-otp/', CreateOTPAPIView.as_view(), name='create_otp'),
    path('get-student-info/', GetStudentInfoAPIView.as_view(), name='get_student_info'),

    # Student
    path('get-student/', GetStudentAPIView.as_view(), name='get_student'),
    path('student-list/', StudentListAPIView.as_view(), name='student_list'),
    path('student-detail/<int:pk>/', StudentDetailAPIView.as_view(), name='student_detail'),
    path('get-student-info/', GetStudentInfoAPIView.as_view(), name='get_student_info'),
    path('create-student/', CreateStudentAPIView.as_view(), name='create_student'),
    path('create-student-by-passport/', CreateStudentByPassportAPIView.as_view(), name='create_student_by_passport'),
    path('update-student-info/', UpdateStudentInfoAPIView.as_view(), name='update_student_info'),

    # Password Reset
    path('auth/reset-password/request/', ResetPasswordRequestAPIView.as_view(), name='reset_password_request'),
    path('auth/reset-password/verify/', VerifyResetCodeAPIView.as_view(), name='verify_reset_code'),
    path('auth/reset-password/confirm/', ResetPasswordConfirmAPIView.as_view(), name='reset_password_confirm'),


    # Study Types TEMPLATE
    path('registration-admin/', student_registration_view, name='student-registration'),
    path('get-program-admin/', GetProgramIDView.as_view(), name='student-program-id'),
    path('get-student-admin/', GetStudentView.as_view(), name='student-get'),
    path('create-student-admin/', StudentCreateView.as_view(), name='student-create-admin'),
    path('create-student-passport-admin/', StudentCreateByPassportView.as_view(), name='student-create-passport'),
    path('update-student-admin/', StudentUpdateView.as_view(), name='student-update'),
    path('create-student-application/', CreateStudentApplication.as_view(), name='create-student-application-admin'),


]
