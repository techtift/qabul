from university.models.faculty import Faculty

def get_faculties(lang='uz'):
    faculties = Faculty.objects.filter(language=lang).select_related('program')
    return faculties