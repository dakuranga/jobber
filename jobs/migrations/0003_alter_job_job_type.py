# Generated by Django 4.2.5 on 2023-09-09 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_rename_job_location_type_job_job_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(choices=[('Full Time', 'FT'), ('Contract', 'Contract'), ('Contract to Hire', 'Contract to Hire')], max_length=20),
        ),
    ]
