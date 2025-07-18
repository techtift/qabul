from university.models.exam import Exam
from university.models.program import Program
from university.models.faculty import Faculty
from university.models.application import Application
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from university.models.study_type import StudyType
from user.models.student import Student

def create_application(application_data):
    title = application_data.get('title')
    description = application_data.get('description')
    program_ids = application_data.get('program_ids', [])
    faculty_ids = application_data.get('faculty_ids', [])
    study_type_ids = application_data.get('study_type_ids', [])
    exam_date_ids = application_data.get('exam_date_ids', [])
    start_date = application_data.get('start_date')
    end_date = application_data.get('end_date')

    programs = Program.objects.filter(id__in=program_ids)   
    if not programs:
        raise CustomApiException(
            message="No valid programs found",
            code=ErrorCodes.NOT_FOUND,
            status_code=404
        )
    faculties = Faculty.objects.filter(id__in=faculty_ids)
    if not faculties:
        raise CustomApiException(
            message="No valid faculties found",
            code=ErrorCodes.NOT_FOUND,
            status_code=404
        )
    study_types = StudyType.objects.filter(id__in=study_type_ids)
    if not study_types:
        raise CustomApiException(
            message="No valid study types found",
            code=ErrorCodes.NOT_FOUND,
            status_code=404
        )
    exams = Exam.objects.filter(id__in=exam_date_ids)
    if not exams:
        raise CustomApiException(
            message="No valid exam dates found",
            code=ErrorCodes.NOT_FOUND,
            status_code=404
        )

    application = Application.objects.create(
        title=title,
        description=description,
        start_date=start_date,
        end_date=end_date
    )
    application.programs.set(programs)
    application.faculties.set(faculties)
    application.study_types.set(study_types)
    application.exams.set(exams)
    application.save()
    
    return application