from university.models.student_dtm import StudentDtmResult
from user.models.student import Student
from core.exceptions.error_messages import  ErrorCodes
from core.exceptions.exception import CustomApiException

def create_student_dtm(student,data):
    """
    Create a new StudentDtmResult instance with the provided data.
    
    Args:
        data (dict): A dictionary containing the student ID and optional dtm_blank file.
    
    Returns:
        StudentDtmResult: The created StudentDtmResult instance.
    """
    student.is_exam_exempt = True
    student.is_attended_exam=True
    student.save(update_fields=['is_exam_exempt','is_attended_exam'])
    dtm_file = data.get('dtm_file')
    StudentDtmResult.objects.create(
        student=student,
        dtm_file=dtm_file
    )
    
    return True 