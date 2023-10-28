from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_management.models import CustomUser
from .models import EmailTemplate
from .models import EmailSignature
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from attachments.forms import AttachmentForm


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

class EmailSignatureForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = EmailSignature
        fields = ['name', 'content']

from ckeditor.widgets import CKEditorWidget
from django import forms
from settings.forms import AttachmentForm
from settings.models import TemplateAttachment
from attachments.models import Attachment
from multiupload.fields import MultiFileField


class EmailTemplateForm(forms.ModelForm):
    attachments = MultiFileField(min_num=0, max_num=5, max_file_size=1024 * 1024 * 5, required=False)

    class Meta:
        model = EmailTemplate
        fields = ['name', 'subject', 'body']

    body = forms.CharField(widget=CKEditorWidget())

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()

        attachments = self.cleaned_data.get('attachments')
        if attachments:
            for attachment in attachments:
                attachment_instance = Attachment(file=attachment)
                attachment_instance.save()
                instance.templateattachment_set.create(attachment=attachment_instance)

        return instance

class UserProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

