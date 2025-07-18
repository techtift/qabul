import pandas as pd
from university.models.question import Question
from university.models.subject import Subject

def import_questions_from_excel(subject_id, file_path, lang='uz'):
    """
    Imports questions from an Excel file and saves them to the Question model,
    ensuring no 'nan' strings are saved.
    """
    subject = Subject.objects.filter(id=subject_id).first()
    if not subject:
        raise ValueError(f"Subject with id={subject_id} not found!")

    df = pd.read_excel(file_path)
    total_created = 0

    for _, row in df.iterrows():
        # Helper to get clean text, avoiding NaN
        def safe_get(val):
            return str(val).strip() if pd.notna(val) and str(val).strip().lower() != "nan" else ""

        question_text = safe_get(row[0])
        version_a = safe_get(row[1])
        version_b = safe_get(row[2])
        version_c = safe_get(row[3])
        version_d = safe_get(row[4])

        # Skip if question_text or version_a is blank
        if not question_text or not version_a:
            continue

        Question.objects.create(
            subject=subject,
            question_text=question_text,
            version_a=version_a,
            version_b=version_b,
            version_c=version_c,
            version_d=version_d,
            is_correct_a=True,
            is_correct_b=False,
            is_correct_c=False,
            is_correct_d=False,
            lang=lang
        )
        total_created += 1

    return total_created
    