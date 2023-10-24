from django import forms

class JobApplicationForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    phone = forms.CharField(label='Phone', max_length=15)
    email = forms.EmailField(label='Email')
    cv = forms.FileField(label='CV', required=True)
    location = forms.CharField(label='Location', max_length=100)
    current_ctc = forms.DecimalField(label='Current CTC', max_digits=10, decimal_places=2)
    expected_ctc = forms.DecimalField(label='Expected CTC', max_digits=10, decimal_places=2)
    notice_period = forms.IntegerField(label='Notice Period (in days)')
    serving_notice_period = forms.ChoiceField(label='Serving Notice Period', choices=[('yes', 'Yes'), ('no', 'No')])
    expected_joining_date = forms.DateField(label='Expected Joining Date')
    linkedin_url = forms.URLField(label='LinkedIn Profile URL', max_length=200)
