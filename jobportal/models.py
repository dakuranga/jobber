from django.db import models
from jobs.models import Job  # Import the Job model from your existing app

class JobListing(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='listing')
    date_published = models.DateTimeField(null=True, blank=True)
    candidates = models.ManyToManyField('candidates.Candidate', blank=True)  # Import the Candidate model from your existing app

    def __str__(self):
        return self.job.job_title
