# Generated by Django 4.2.6 on 2023-10-23 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0018_alter_candidate_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='source',
            field=models.CharField(choices=[('recruiter', 'Sourced by Recruiter'), ('application', 'Incoming Application')], default='application', max_length=20),
        ),
    ]
