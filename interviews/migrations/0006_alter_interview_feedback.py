# Generated by Django 4.2.5 on 2023-09-19 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0005_interviewstagechange'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='feedback',
            field=models.TextField(default='Pending', max_length=255),
        ),
    ]
