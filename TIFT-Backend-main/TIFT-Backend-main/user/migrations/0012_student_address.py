# Generated by Django 5.1.3 on 2025-06-29 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_student_is_exam_exempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
