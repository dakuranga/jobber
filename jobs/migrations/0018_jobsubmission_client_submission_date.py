# Generated by Django 4.2.5 on 2023-09-19 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0017_jobsubmission_previous_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobsubmission',
            name='client_submission_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
