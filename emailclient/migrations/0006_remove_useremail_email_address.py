# Generated by Django 4.2.6 on 2023-10-24 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailclient', '0005_useremail_token_expiration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useremail',
            name='email_address',
        ),
    ]
