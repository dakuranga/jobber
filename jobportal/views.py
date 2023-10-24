from django.shortcuts import render, redirect, get_object_or_404
from jobportal.models import JobListing
from jobs.models import Job
from candidates.models import Candidate

from django.utils import timezone

# views.py
from django.http import JsonResponse

from django.http import JsonResponse

def publish_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    # Check if a JobListing instance already exists for this Job
    job_listing, created = JobListing.objects.get_or_create(job=job)
    
    if created:
        job_listing.date_published = timezone.now()
        job_listing.save()
        # Additional logic for handling job attachment and other fields
        # You can extract text from the PDF and save it as job description here
        return JsonResponse({'message': 'Job published successfully'})
    else:
        return JsonResponse({'message': 'Job is already published'})


from django.http import JsonResponse

def unpublish_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    # Check if a JobListing instance exists for this Job
    try:
        job_listing = JobListing.objects.get(job=job)
        job_listing.delete()  # Delete the JobListing instance
        return JsonResponse({'message': 'Job unpublished successfully'})
    except JobListing.DoesNotExist:
        return JsonResponse({'message': 'Job is not published'})


def job_listing(request):
    jobs = JobListing.objects.filter(job__job_status='Open')
    return render(request, 'job_listing.html', {'jobs': jobs})


from django.shortcuts import render, get_object_or_404
from .models import JobListing
from .forms import JobApplicationForm
from candidates.models import Candidate
import bleach
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse



def job_detail_and_apply(request, job_id):
    job = get_object_or_404(JobListing, job_id=job_id)

    
    if request.method == 'POST':
        # Handle the submitted application form
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            serving_notice_period = True if form.cleaned_data['serving_notice_period'] == 'yes' else False

            # Create and save a Candidate instance without sanitization
            candidate = Candidate(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                cv=form.cleaned_data['cv'],
                location=form.cleaned_data['location'],
                current_ctc=form.cleaned_data['current_ctc'],
                expected_ctc=form.cleaned_data['expected_ctc'],
                notice_period=form.cleaned_data['notice_period'],
                serving_notice_period=serving_notice_period,  # Map "yes" and "no" to True and False
                expected_joining_date=form.cleaned_data['expected_joining_date'],
                linkedin_url=form.cleaned_data['linkedin_url'],
                source='application', 
            )
            candidate.save()

            success_message = 'Your application has been submitted successfully.'


            return HttpResponseRedirect(reverse('job_listing') + '?success_message=' + success_message)

        

    else:
        # Display the job details and application form
        form = JobApplicationForm()
    
    return render(request, 'job_detail_and_apply.html', {'job': job, 'form': form})






# your_app/management/commands/change_candidate_source.py

from django.core.management.base import BaseCommand
from candidates import Candidate  # Update with your actual app name

class Command(BaseCommand):
    help = 'Change the source field of all candidates to "recruiter"'

    def handle(self, *args, **kwargs):
        try:
            Candidate.objects.update(source='recruiter')
            self.stdout.write(self.style.SUCCESS('Successfully updated source field to "recruiter" for all candidates.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {str(e)}'))
