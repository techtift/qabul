# Generated by Django 5.1.3 on 2025-06-01 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='passport_number',
            new_name='pnfl',
        ),
    ]
