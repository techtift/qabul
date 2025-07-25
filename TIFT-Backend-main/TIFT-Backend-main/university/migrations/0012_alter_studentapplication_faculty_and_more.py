# Generated by Django 5.1.3 on 2025-06-02 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0011_remove_faculty_price_faculty_day_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentapplication',
            name='faculty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_applications', to='university.faculty'),
        ),
        migrations.AlterField(
            model_name='studentapplication',
            name='study_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_applications', to='university.studytype'),
        ),
    ]
