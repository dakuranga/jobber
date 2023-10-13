from django import forms
from django.core.exceptions import ValidationError
from .models import Candidate
from jobs.models import Job

class CandidateForm(forms.ModelForm):
    # Define choices for the serving_notice_period field
    serving_notice_period = forms.BooleanField(
        required=False, 
        widget=forms.Select(choices=[(True, 'Yes'), (False, 'No')])
    )


    def clean_cv(self):
        cv = self.cleaned_data.get('cv', False)
        if cv:
            filename = cv.name
            if not filename.endswith(('.doc', '.docx', '.pdf')):
                raise ValidationError("Invalid file format. Please upload a Word or PDF document.")
        return cv

    class Meta:
        model = Candidate
        fields = '__all__'


from django import forms
from jobs.models import JobSubmission, Job


class JobSubmissionForm(forms.ModelForm):
    job = forms.ModelChoiceField(queryset=Job.objects.all())

    class Meta:
        model = JobSubmission
        fields = ['job']


from jobs.models import JobSubmission

class UpdateStageForm(forms.ModelForm):

    class Meta:
        model = JobSubmission
        fields = ['stage']

class CVImportForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['cv']


from django import forms
from candidates.models import Candidate
from jobs.models import JobSubmission

class CandidateSubmissionForm(forms.ModelForm):
    candidate = forms.ModelChoiceField(queryset=Candidate.objects.all())

    class Meta:
        model = JobSubmission
        fields = ['candidate']  # Add other necessary fields if needed


