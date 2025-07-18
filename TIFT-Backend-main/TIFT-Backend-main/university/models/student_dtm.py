from core.models.basemodel import SafeBaseModel
from user.models.student import Student
from django.db import models



class StudentDtmResult(SafeBaseModel):
    student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='dtm_results')
    dtm_file=models.FileField(upload_to='dtm_file', blank=True, null=True)
    