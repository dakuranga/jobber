# Generated by Django 4.2.5 on 2023-09-09 11:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_alter_job_job_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
