from django.urls import path
from university.views.programs.get_programs import GetProgramsAPIView
from university.views.faculties.get_faculties import GetFacultiesAPIView
from university.views.faculties.get_faculities_by_program import GetFacultiesByProgramAPIView
from university.views.exams.get_exams import GetExamsAPIView
from university.views.applications.get_applications import GetApplicationsAPIView
from university.views.applications.create_student_application import CreateStudentApplicationAPIView
from university.views.applications.get_student_applications import GetStudentApplicationsAPIView
from university.views.programs.get_study_types import GetProgramsStudyTypesAPIView
from university.views.questions.get_questions_by_faculty import GetQuestionsByFacultyAPIView
from university.views.questions.check_questions import CheckQuestionsAPIView
from university.views.questions.check_exam_valid_date import CheckExamValidDateAPIView
from university.views.read_file.build_file_url import BuildFileUrlAPIView
from university.views.generate_contract.generate_contract import GenerateContractAPIView, GenerateCertificateAPIView
from university.views.study_duration.get_study_duration import GetStudyDurationAPIView
from university.views.study_types.get_study_types import  GetProgramsFacultyStudyTypesAPIView
from university.views.student_dtm.create_student_dtm import StudentDtmAPIView
urlpatterns = [
    path('programs/', GetProgramsAPIView.as_view(), name='get_programs'),
    path('programs/study-types/', GetProgramsStudyTypesAPIView.as_view(), name='get_programs'),
    path('study-duration/', GetStudyDurationAPIView.as_view(), name='get_study_duration'),
    path('faculties/', GetFacultiesAPIView.as_view(), name='get_faculties'),
    path('study-types/', GetProgramsFacultyStudyTypesAPIView.as_view(), name='get_study_types'),

    path('faculties/program/', GetFacultiesByProgramAPIView.as_view(), name='get_study_type_by_program'),
    path('exams/', GetExamsAPIView.as_view(), name='get_exams'),
    path('applications/', GetApplicationsAPIView.as_view(), name='list_applications'),
    path('student-applications/create/', CreateStudentApplicationAPIView.as_view(), name='create_student_application'),
    path('student-applications/', GetStudentApplicationsAPIView.as_view(), name='get_student_applications'),
    path('questions/faculty/', GetQuestionsByFacultyAPIView.as_view(), name='get_questions_by_faculty'),
    path('questions/check/', CheckQuestionsAPIView.as_view(), name='check_questions'),
    path('questions/check-exam-valid-date/', CheckExamValidDateAPIView.as_view(), name='check_exam_valid_date'),
    path('file/build-url/', BuildFileUrlAPIView.as_view(), name='build_file_url'),
    path('generate-contract/', GenerateContractAPIView.as_view(), name='generate_contract'),
    path('generate-certificate/', GenerateCertificateAPIView.as_view(), name='generate_certificate'),
    
    
    path('student-dtm/', StudentDtmAPIView.as_view(), name='create_student_dtm'),
]
