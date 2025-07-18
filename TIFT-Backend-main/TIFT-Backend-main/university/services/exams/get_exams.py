from university.models.exam import Exam


def get_exams_by_program_or_faculty(program_id=None, faculty_id=None):
    from django.db.models import Q
    exams = Exam.objects.all()
    if program_id and faculty_id:
        exams = exams.filter(Q(program_id=program_id) | Q(faculty_id=faculty_id))
    elif program_id:
        exams = exams.filter(program_id=program_id)
    elif faculty_id:
        exams = exams.filter(faculty_id=faculty_id)
    exams = exams.select_related('program', 'faculty')
    result = []
    for exam in exams:
        result.append({
            "id": exam.id,
            "is_online": exam.is_online,
            "exam_type": getattr(exam, "exam_type", None),  # <-- Only if this exists!
            "exam_date": exam.exam_date,
            "program": {"id": exam.program.id, "name": exam.program.name} if exam.program else None,
            "faculty": {"id": exam.faculty.id, "name": exam.faculty.name} if exam.faculty else None,
        })
    return result