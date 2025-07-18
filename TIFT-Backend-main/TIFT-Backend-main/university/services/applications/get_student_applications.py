from university.models.program import Program
from university.models.faculty import Faculty
from university.models.application import StudentApplication
from user.models.user import User
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes

def get_student_applications(student_id=None, program_id=None, faculty_id=None):
    student_applications = StudentApplication.objects.all()
    if student_id:
        student_applications = student_applications.filter(student_id=student_id)
    if program_id:
        student_applications = student_applications.filter(program_id=program_id)
    if faculty_id:
        student_applications = student_applications.filter(faculty_id=faculty_id)
    student_applications = student_applications.select_related('program', 'faculty', 'student', 'study_type', 'exam_date')
    return student_applications