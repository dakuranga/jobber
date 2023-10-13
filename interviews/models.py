from django.db import models
from user_management.models import CustomUser
from jobs.models import JobSubmission

class Interview(models.Model):
    INTERVIEW_MODES = [
        ('Online', 'Online'),
        ('Face-to-Face', 'Face-to-Face'),
        ('Telephone', 'Telephone')
    ]

    submission = models.ForeignKey(JobSubmission, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mode = models.CharField(max_length=20, choices=INTERVIEW_MODES, null=True, blank=True)
    interviewer = models.CharField(max_length=255, null=True, blank=True)
    interview_date = models.DateField(null=True, blank=True)
    interview_time = models.CharField(max_length=10, null=True, blank=True) 
    feedback = models.TextField(max_length=255, default="Pending")
    
    stage = models.CharField(max_length=20, choices=JobSubmission.STAGE_CHOICES)



    @property
    def scheduled_date(self):
        return self.submission.stage_changed_date
    
    @property
    def calculated_feedback(self):
        end_statuses = ['Shortlisted', 'Interview Reject', 'Joined']

    # Fetching the latest interview for the submission
        latest_interview = Interview.objects.filter(submission=self.submission).order_by('-id').first()

    # If this interview instance is the latest one for the submission
        if self == latest_interview:
        # If the submission stage is an end status
            if self.submission.stage in end_statuses:
                return self.submission.stage
        # If the submission stage isn't an end status
            else:
                return self.feedback  # This should be "Pending" for the latest interview not resulting in an end status

    # For older interview instances (not the latest one for the submission)
        else:
            if self.stage == 'L1 Interview':
            # If there's a subsequent L2 interview
                if Interview.objects.filter(submission=self.submission, stage='L2 Interview').exists():
                    return "Moved to L2"
            # If the submission stage is an end status after L1
                elif self.submission.stage in end_statuses:
                    return self.feedback
                else:
                    return "Pending"

            elif self.stage == 'L2 Interview':
            # If there's a subsequent L3 interview
                if Interview.objects.filter(submission=self.submission, stage='L3 Interview').exists():
                    return "Moved to L3"
            # If the submission stage is an end status after L2
                elif self.submission.stage in end_statuses:
                    return self.feedback
                else:
                    return "Pending"
        
            elif self.stage == 'L3 Interview':
                return self.feedback





    


    

    def __str__(self):
        return f"Interview for {self.submission.candidate.name} with {self.interviewer or 'TBD'} on {self.interview_date or 'TBD'} at {self.interview_time or 'TBD'}"




from django.db import models
from datetime import datetime

# ... other model imports ...

class InterviewStageChange(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    stage = models.CharField(max_length=50)  # L1 Interview, L2 Interview, etc.
    changed_date = models.DateTimeField(default=datetime.now)
