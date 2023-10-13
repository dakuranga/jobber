from django import forms
from django.core.exceptions import ValidationError
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
    
    def clean_about_client_attachment(self):
        about_client_attachment = self.cleaned_data.get('about_client_attachment', False)
        if about_client_attachment:
            filename = about_client_attachment.name
            if not filename.lower().endswith(('.doc', '.docx', '.pdf')):
                raise ValidationError("Invalid file format. Please upload a Word or PDF document.")
        return about_client_attachment
