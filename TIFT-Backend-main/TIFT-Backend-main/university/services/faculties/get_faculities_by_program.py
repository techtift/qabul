from university.models.program import Program
from university.models.faculty import Faculty

def get_faculties_by_program(program_id=None):
    # If a program_id is provided, filter by it; else get all programs
    programs_qs = Program.objects.all()
    if program_id:
        programs_qs = programs_qs.filter(id=program_id)

    # Prefetch faculties for efficiency
    programs = programs_qs.prefetch_related('faculties')

    result = []
    for program in programs:
        faculties = [
            {'id': faculty.id, 'name': faculty.name}
            for faculty in program.faculties.all()
        ]
        result.append({
            'id': program.id,
            'name': program.name,
            'faculties': faculties
        })
    return result