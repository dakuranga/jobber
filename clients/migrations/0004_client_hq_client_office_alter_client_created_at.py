# Generated by Django 4.2.5 on 2023-09-11 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_client_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='hq',
            field=models.CharField(default='Delhi', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='office',
            field=models.CharField(default='delhi', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]