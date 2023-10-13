# Generated by Django 4.2.5 on 2023-09-09 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_job_date_added'),
        ('candidates', '0005_alter_candidate_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='jobs',
            field=models.ManyToManyField(blank=True, to='jobs.job'),
        ),
    ]
