# Generated by Django 4.2.5 on 2023-09-19 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0003_interview_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='feedback',
            field=models.TextField(blank=True, default='Pending', max_length=255, null=True),
        ),
    ]
