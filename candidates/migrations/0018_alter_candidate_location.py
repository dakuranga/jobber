# Generated by Django 4.2.5 on 2023-09-11 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0017_alter_candidate_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]