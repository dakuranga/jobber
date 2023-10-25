from django.db import models
from user_management.models import CustomUser


class EmailTemplate(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.name


from django.db import models
from django.contrib.auth.models import User

class UserEmail(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=200)  # Store the OAuth access token
    refresh_token = models.CharField(max_length=200, blank=True, null=True)  # Store the OAuth refresh token (if available)
    token_expiration = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.email_address
