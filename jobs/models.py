from django.db import models
from clients.models import Client
from candidates.models import Candidate
from django.utils import timezone 


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('FT', 'FT'),
        ('Cont', 'Con'),
        ('C2H', 'C2H'),
    ]
    JOB_STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Hold', 'Hold'),
        ('Upcoming', 'Upcoming'),
    ]
    MODE_CHOICES = [
        ('Hybrid', 'Hybrid'),
        ('Remote', 'Remote'),
        ('Onsite', 'Onsite'),
    ]
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    job_notes = models.TextField()
    job_location = models.CharField(max_length=100)
    job_mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    job_status = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES, default='Open')  
    job_work_hours = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    job_priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    job_attachment = models.FileField(upload_to='job_attachments/', blank=True, null=True)
    job_minimum_experience = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    candidates = models.ManyToManyField(Candidate, through='JobSubmission')

    def __str__(self):
        return self.job_title



    
from user_management.models import CustomUser

from jobs.models import Job
class JobSubmission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_client_submitted = models.DateTimeField(blank=True, null=True)
    previous_stage = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        unique_together = ('job', 'candidate') 
    
    STAGE_CHOICES = [
        ('Internal', 'Internal'),
        ('Client Submission', 'Client Submission'),
        ('QC Reject', 'QC Reject'),
        ('L1 Interview', 'L1 Interview'),
        ('L2 Interview', 'L2 Interview'),
        ('L3 Interview', 'L3 Interview'),
        ('Interview Reject', 'Interview Reject'),
        ('Shortlisted', 'Shortlisted'),
        ('Joined', 'Joined')
    ]
    
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='Internal')
    stage_changed_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.candidate.name}"



from django.shortcuts import redirect, get_object_or_404
from .models import JobSubmission

def update_submission_stage(request, submission_id, stage):
    print(f"Updating stage for submission ID {submission_id} to {stage}")
    submission = get_object_or_404(JobSubmission, id=submission_id)
    if submission.stage != stage:  # Check if the stage is actually changing
        print(f"Stage is changing from {submission.stage} to {stage}")
        submission.stage = stage
        submission.save()
        JobSubmissionHistory.objects.create(
            job_submission=submission,
            stage=stage,
            changed_at=timezone.now()  # Record the current time
        )
    return redirect('job_details', job_id=submission.job.id)


from django.db import models
from django.utils import timezone

class JobSubmissionHistory(models.Model):
    job_submission = models.ForeignKey(JobSubmission, related_name='histories', on_delete=models.CASCADE)
    stage = models.CharField(max_length=20)
    changed_at = models.DateTimeField()
    

    def __str__(self):
        return f"Changed to {self.stage} at {self.changed_at}"
    




