
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from university.models.faculty import Faculty
from university.models.question import Question
from university.models.application import StudentApplication
import random
from collections import defaultdict

def get_questions_by_faculty(user_id):
    student_application = StudentApplication.objects.filter(student__user_id=user_id).first()
    if not student_application:
        raise CustomApiException(ErrorCodes.NOT_FOUND, "Student application not found")

    subjects = list(student_application.faculty.subjects.all())
    if not subjects:
        raise CustomApiException(ErrorCodes.NOT_FOUND, "No subjects found for this faculty")

    subject_count = len(subjects)

    if 20 % subject_count != 0:
        raise CustomApiException(ErrorCodes.VALIDATION_ERROR, "Total questions must be divisible by number of subjects")

    questions_per_subject = 20 // subject_count

    grouped = []

    for subject in subjects:
        all_questions = list(
            Question.objects.filter(subject=subject, lang=student_application.lang)
        )
        if len(all_questions) < questions_per_subject:
            raise CustomApiException(ErrorCodes.NOT_FOUND, f"Not enough questions for subject {subject.name}")

        selected = random.sample(all_questions, questions_per_subject)

        grouped.append({
            'subject_id': subject.id,
            'subject_name': subject.name,
            'questions': [{
                'id': q.id,
                'question_text': q.question_text,
                'version_a': q.version_a,
                'version_b': q.version_b,
                'version_c': q.version_c,
                'version_d': q.version_d,
            } for q in selected]
        })

    return grouped