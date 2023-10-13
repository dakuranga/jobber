from django.db import models
from django.conf import settings 



class Candidate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    cv = models.FileField(upload_to='CV_All/')
    location = models.CharField(max_length=200, blank=True, null=True)
    current_ctc = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    expected_ctc = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    notice_period = models.PositiveIntegerField(help_text="In days", blank=True, null=True)
    serving_notice_period = models.BooleanField(default=False, blank=True, null=True)
    last_working_day = models.CharField(max_length=200, blank=True, null=True)
    expected_joining_date = models.CharField(max_length=200, blank=True, null=True)
    total_experience = models.PositiveIntegerField(help_text="In years", blank=True, null=True)
    relevant_experience = models.PositiveIntegerField(help_text="In years", blank=True, null=True)
    reason_for_change = models.CharField(max_length=200, blank=True, null=True)
    linkedin_url = models.CharField(max_length=200, blank=True, null=True, default=None)
    recruiter_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    

   
    def __str__(self):
        return self.name

