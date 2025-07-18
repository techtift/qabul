from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from university.models.application import Application
from university.models.program import Program
from university.services.applications.create_student_application import create_student_application
from university.services.programs.get_study_types import get_study_types
from university.services.faculties.get_faculities_by_program import get_faculties_by_program
from user.admin_services.create_user_admin import create_user_admin
from user.models.student import Student
from user.services.create_student_by_passport import student_create_by_passport_service
from user.services.update_student_info import update_student_info_service


def student_registration_view(request):
    programs = Program.objects.all()

    context = {
        'programs': programs,
    }
    return render(request, 'user/student_form.html', context)
class GetProgramIDView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # CSRF va auth yo‘q

    def post(self, request, *args, **kwargs):
        program_id = request.data.get('program_id')  # request.POST emas
        data = {}

        if program_id:
            data['program_id'] = program_id
            study_types = get_study_types(program_id)
            study_faculties = get_faculties_by_program(program_id)
            data['study_types'] = list(study_types.values('id', 'name'))
            data['study_faculties'] = study_faculties

        return Response(data)


class GetStudentView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # CSRF va auth yo‘q

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        data = {}

        if user_id:
            try:
                student = Student.objects.get(user_id=user_id)
                data['student'] = {
                    "user_id": student.id,
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "father_name": student.father_name,
                    "birth_date": student.birth_date,
                    "birth_place": student.birth_place,
                    "citizenship": student.citizenship,
                    "pinfl": student.pinfl,
                    "passport_number": student.passport_number,
                    "gender": student.gender,
                    "qualification": student.qualification,
                    "name_qualification": student.name_qualification,
                    "photo": student.photo.url if student.photo else None,
                }
            except Student.DoesNotExist:
                data['student'] = None

        return Response(data)
@method_decorator(csrf_exempt, name='dispatch')
class StudentCreateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        data = {}
        phone_number = request.data.get("phone_number")
        if phone_number:
            user = create_user_admin(phone_number)
            data['user_id'] = user.id
        return Response(data)

class StudentCreateByPassportView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        data = {}

        dob = request.data.get("dob")
        passport = request.data.get("passport")
        user_id = request.data.get("user_id")

        if dob and passport and user_id:
            response = student_create_by_passport_service(dob, passport, user_id)

            data['student'] = {
                "user_id": response.id,
                "first_name": response.first_name,
                "last_name": response.last_name,
                "father_name": response.father_name,
                "birth_date": response.birth_date,
                "birth_place": response.birth_place,
                "citizenship": response.citizenship,
                "pinfl": response.pinfl,
                "passport_number": response.passport_number,
                "gender": response.gender,
                "qualification": response.qualification,
                "name_qualification": response.name_qualification,
                "photo": response.photo.url if response.photo else None,
            }

        return Response(data)


class StudentUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        data = request.data.copy()

        if 'diploma' in request.FILES:
            data['diploma'] = request.FILES['diploma']

        update_student_info_service(user_id, data)
        return Response({"success": True})


class CreateStudentApplication(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        lang = request.data.get("lang")
        is_transfer = request.data.get("is_transfer") == "True"
        application = Application.objects.first()
        if not application:
            return Response({"ok": False, "detail": "Hech qanday application mavjud emas"}, status=400)
        application_id = application.id
        if is_transfer:
            transfer_level = request.data.get("transfer_level")
            program_id = request.data.get("program_id")
            faculty_id = request.data.get("faculty_id")
            transcript = request.FILES.get("transcript")
            data={
                "application_id":application_id,
                "lang":lang,
                "is_transfer":True,
                "transfer_level":transfer_level,
                "program_id":program_id,
                "faculty_id":faculty_id,
                "transcript":transcript,
                "admin_added_student":True,
            }
            response = create_student_application(data,user_id)

        else:
            study_type_id = request.data.get("study_type_id")
            program_id = request.data.get("program_id")
            faculty_id = request.data.get("faculty_id")
            data={
                "application_id":application_id,
                "study_type_id":study_type_id,
                "program_id":program_id,
                "faculty_id":faculty_id,
                "lang":lang,
                "admin_added_student":True,
            }
            response = create_student_application(data,user_id)

        return Response({"ok": True, "detail":"good"}, status=200)

