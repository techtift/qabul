from university.models.program import Program

def get_study_types(program_id):
    try:
        program = Program.objects.get(id=program_id)
        return program.study_types.all()
    except Program.DoesNotExist:
        return []
