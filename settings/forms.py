from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_management.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # Define custom labels for fields
    is_active = forms.BooleanField(
        label="Activate their account",  # Custom label for is_active field
        required=False,  # Set required to False if you want to allow it to be unchecked
    )
    is_superuser = forms.BooleanField(
        label="Manager",  # Custom label for is_staff field
        required=False,  # Set required to False if you want to allow it to be unchecked
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'is_active', 'is_superuser')

