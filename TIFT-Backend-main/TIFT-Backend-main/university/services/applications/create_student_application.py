from university.models.exam import Exam
from university.models.program import Program
from university.models.faculty import Faculty
from university.models.application import Application, StudentApplication
from university.models.study_type import StudyType
from user.models.user import User
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from user.models.student import Student

def create_student_application(application_data, user_id: int) -> StudentApplication:
    application_id   = application_data.get('application_id')
    program_id       = application_data.get('program_id')
    faculty_id       = application_data.get('faculty_id')
    is_transfer      = application_data.get('is_transfer', False)
    transfer_level   = application_data.get('transfer_level')
    study_type_id    = application_data.get('study_type_id')
    exam_date_id     = application_data.get('exam_date_id')
    transcript       = application_data.get('transcript')
    is_online_exam   = application_data.get('is_online_exam', True)
    lang             = application_data.get('lang', 'uz')
    admin_added_student = application_data.get('admin_added_student', False)

    # Duplicate check
    if StudentApplication.objects.filter(application_id=application_id, student__user_id=user_id).exists():
        raise CustomApiException(
            ErrorCodes.ALREADY_EXISTS,
            "You already have an application for this program."
        )

    # Core lookups
    application = Application.objects.filter(id=application_id).first()
    if not application:
        raise CustomApiException(ErrorCodes.NOT_FOUND, "Application not found.")
    program = Program.objects.filter(id=program_id).first()
    if not program:
        raise CustomApiException(ErrorCodes.NOT_FOUND, "Program not found.")


    study_type = None
    if study_type_id is not None:
        study_type = StudyType.objects.filter(id=study_type_id).first()
        if not study_type:
            raise CustomApiException(ErrorCodes.NOT_FOUND, "Study type not found.")

    # Optional exam date
    exam_date = None
    if exam_date_id is not None:
        exam_date = Exam.objects.filter(id=exam_date_id).first()
        if not exam_date:
            raise CustomApiException(ErrorCodes.NOT_FOUND, "Exam date not found.")

    # User & student
    student_user = User.objects.filter(id=user_id).first()
    if not student_user:
        raise CustomApiException(ErrorCodes.NOT_FOUND, "User not found.")
    student = Student.objects.filter(user_id=user_id).first()
    if not student:
        raise CustomApiException(ErrorCodes.NOT_FOUND, "Student record not found.")
    if program_id == 29:
        student.is_attended_exam=True
        student.is_exam_exempt=True


    # Transfer-specific logic
    if is_transfer:
        student.is_attended_exam = True
        student.is_exam_exempt = True
        if not transfer_level:
            raise CustomApiException(
                ErrorCodes.INVALID_INPUT,
                "transfer_level is required for transfer applications."
            )
        if not transcript:
            raise CustomApiException(
                ErrorCodes.INVALID_INPUT,
                "transcript is required for transfer applications."
            )
        # skip faculty entirely for transfer
        faculty = None

    else:
        # non-transfer must supply a valid faculty
        if not faculty_id:
            raise CustomApiException(
                ErrorCodes.INVALID_INPUT,
                "faculty_id is required unless this is a transfer."
            )
        faculty = Faculty.objects.filter(id=faculty_id).first()
        if not faculty:
            raise CustomApiException(
                ErrorCodes.NOT_FOUND,
                "Faculty not found."
            )
    if admin_added_student:
        student.is_passed_exam = True
        student.is_attended_exam = True
        student.save()
    if student.is_attended_exam or student.is_exam_exempt:
        student.save()
    # Finally create
    student_app = StudentApplication.objects.create(
        student         = student,
        application     = application,
        program         = program,
        faculty         = faculty,
        study_type      = study_type,
        is_online_exam  = is_online_exam,
        exam_date       = exam_date,
        is_transfer     = is_transfer,
        transfer_level  = transfer_level if is_transfer else None,
        transcript      = transcript if is_transfer else None,
        lang            = lang,
    )
    return student_app
