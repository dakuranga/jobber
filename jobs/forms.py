from django import forms
from django.core.exceptions import ValidationError
from .models import Job, Client
from urllib.parse import urlencode


class JobForm(forms.ModelForm):



    class Meta:
        model = Job
        fields = '__all__'
        widgets = {
            'job_status': forms.Select(choices=Job.JOB_STATUS_CHOICES),
            'job_mode': forms.Select(choices=Job.MODE_CHOICES),
            'job_type': forms.Select(choices=Job.JOB_TYPE_CHOICES),  
            'job_priority': forms.Select(choices=Job.PRIORITY_CHOICES),
            

        }

        

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

        # Exclude the 'candidates' field from the form
        self.fields.pop('candidates')

    def clean_job_attachment(self):
        job_attachment = self.cleaned_data.get('job_attachment', False)
        if job_attachment:
            filename = job_attachment.name
            if not filename.endswith(('.doc', '.docx', '.pdf')):
                raise ValidationError("Invalid file format. Please upload a Word or PDF document.")
        return job_attachment
    



class JobFilterForm(forms.Form):
    job_status = forms.ChoiceField(choices=[('','Select Status')]+list(Job.JOB_STATUS_CHOICES), required=False)
    job_priority = forms.ChoiceField(choices=[('','Select Priority')]+list(Job.PRIORITY_CHOICES), required=False)
    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False, empty_label="Select Client")

    def urlencode(self):
        data = self.cleaned_data
        query_pairs = []
        for name, value in data.items():
            if value:
                query_pairs.append((name, str(value)))
        return urlencode(query_pairs)


