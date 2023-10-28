from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from attachments.models import Attachment



class EmailTemplate(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subject = models.CharField(max_length=255)
    body = RichTextField()

    def __str__(self):
        return self.name

class TemplateAttachment(Attachment):
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)

class EmailSignature(models.Model):
    name = models.CharField(max_length=200)
    content = RichTextField()
