from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from university.models.application import StudentApplication
from django.utils import timezone


def check_exam_valid_date(student_id: int) -> bool:
    """
    Returns True if there exists a StudentApplication for this student
    whose Application.start_date <= now <= Application.end_date; otherwise False.
    Raises NOT_FOUND if the StudentApplication does not exist.
    """
    now = timezone.now()

    student_application = StudentApplication.objects.filter(student_id=student_id).first()
    if not student_application:
        raise CustomApiException(
            ErrorCodes.NOT_FOUND,
            "Student application not found."
        )

    # Fetch the single Application instance linked to this StudentApplication:
    application = student_application.application
    if not application:
        # (Technically shouldn’t happen if your ForeignKey is not nullable,
        # but guard just in case.)
        raise CustomApiException(
            ErrorCodes.NOT_FOUND,
            "Linked application record is missing."
        )
    if student_application.student.is_attended_exam:
        raise CustomApiException(
            ErrorCodes.VALIDATION_FAILED,
            "Student has already attended the exam."
        )
    if student_application.student.is_passed_exam:
        raise CustomApiException(
            ErrorCodes.VALIDATION_FAILED,
            "Student has already passed the exam."
        )
    # Check if now is between start_date and end_date (inclusive):
    if application.start_date <= now <= application.end_date:
        return True
    return False
