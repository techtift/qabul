from university.models.study_type_many_to_many import StudyTypeFaculty



def get_study_types(faculty_id, program_id):
    qs=StudyTypeFaculty.objects.filter(faculty_id=faculty_id, program_id=program_id).first()
    qs=qs.study_type.all()
    return qs