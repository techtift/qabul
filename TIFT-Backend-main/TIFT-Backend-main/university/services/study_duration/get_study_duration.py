from university.models.duration import Duration



def get_study_duration(faculty_id, study_type_id):
    return Duration.objects.filter(faculty_id=faculty_id, study_type_id=study_type_id).values_list('study_duration', flat=True).first()
