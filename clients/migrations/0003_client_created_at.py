from django.db import migrations, models
from django.utils import timezone  # Import the timezone module

class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_client_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='created_at',
            field=models.DateTimeField(default=timezone.now),  # Set the default value to the current time
            preserve_default=False,
        ),
    ]
