from django import forms
from .models import Interview

class InterviewDetailsForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interview_date', 'interview_time', 'interviewer', 'mode']
