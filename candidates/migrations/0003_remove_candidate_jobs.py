# Generated by Django 4.2.5 on 2023-09-08 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0002_alter_candidate_jobs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='jobs',
        ),
    ]
