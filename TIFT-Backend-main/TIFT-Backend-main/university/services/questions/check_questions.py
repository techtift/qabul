from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from university.models.application import StudentApplication
from university.models.question import Question
from core.utils import send_sms_message
from user.models.sms import UserSMS

def check_questions(user_id, data):
    if not isinstance(data, list):
        raise CustomApiException(ErrorCodes.INVALID_INPUT, "Answers should be a list.")

    correct_count = 0

    for ans in data:
        question_id = ans.get('question_id')
        selected = ans.get('selected')
        if not question_id or selected not in ('a', 'b', 'c', 'd'):
            raise CustomApiException(ErrorCodes.INVALID_INPUT, f"Invalid answer data: {ans}")

        question = Question.objects.filter(id=question_id).first()
        if not question:
            raise CustomApiException(ErrorCodes.NOT_FOUND, f"Question {question_id} not found.")

        is_correct = getattr(question, f'is_correct_{selected}', False)
        if is_correct:
            correct_count += 1

    total = 20
    score_percent = (correct_count / total) * 100 if total else 0
    passed = round(score_percent, 2) >= 10

    student_application = StudentApplication.objects.filter(student__user_id=user_id).first()
    if not student_application:
        raise CustomApiException(ErrorCodes.NOT_FOUND, "Student application not found.")

    # Save exam status and score
    student_application.student.is_attended_exam = True
    student_application.student.is_passed_exam = passed
    student_application.student.save()

    student_application.score = correct_count
    student_application.save()

    if passed:
        message = f"Siz imtihondan muvaffaqiyatli o'tdingiz. \nShartnomani profilingizdan yuklab oling. \nhttps://qabul.tift.uz"

        # Send SMS to the student if they passed
        user_sms = UserSMS.objects.create(
            user=student_application.student.user,
            text=message,
            category='info'
        )

        response = send_sms_message(
            phone=student_application.student.user.phone_number,
            message=message
        )
        if response.status_code == 200:
            user_sms.is_sent = True
            user_sms.save()

    return {
        "total": total,
        "correct": correct_count,
        "score_percent": round(score_percent, 2),
        "passed": True
    }

