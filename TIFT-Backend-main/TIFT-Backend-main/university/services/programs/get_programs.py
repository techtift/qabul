from university.models.program import Program

def get_programs(lang='uz'):
    programs = Program.objects.all()
    return programs
