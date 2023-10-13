from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse  # Add this import statement
from candidates.models import Candidate
from django.utils import timezone 

def reports(request):
    total_candidates_indb = Candidate.objects.count()

    context = {

        'total_candidates_indb': total_candidates_indb
    }
    return render(request, 'reports.html', context)

import csv
from django.http import HttpResponse
from django.shortcuts import render
from candidates.models import Candidate

# View for the export page
def export_candidates_page(request):
    return render(request, 'reports.html')

# View for exporting candidates as CSV
def export_candidates_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="candidates.csv"'

    writer = csv.writer(response)

    # Get all field names for the Candidate model
    candidate_fields = [field.name for field in Candidate._meta.fields]

    # Write the field names as headers
    writer.writerow(candidate_fields)

    candidates = Candidate.objects.all()
    for candidate in candidates:
        # Create a list of values for each field in the same order as the headers
        candidate_data = [getattr(candidate, field) for field in candidate_fields]

        # Write the data to the CSV row
        writer.writerow(candidate_data)

    return response

import csv
import io
import os
import zipfile
from django.http import HttpResponse
from candidates.models import Candidate

def export_candidates_zip(request):
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="candidates.zip"'

    # Create a ZIP file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        candidates = Candidate.objects.all()
        for candidate in candidates:
            cv_file_path = candidate.cv.path
            cv_filename = os.path.basename(cv_file_path)
            zipf.write(cv_file_path, cv_filename)

    # Write the ZIP file to the response
    zip_buffer.seek(0)
    response.write(zip_buffer.read())

    return response

# views.py

import csv
from django.http import HttpResponse
from django.shortcuts import render
from jobs.models import Job

def export_jobs_page(request):
    return render(request, 'reports.html')

def export_jobs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="jobs.csv"'

    writer = csv.writer(response)

    # Get all field names for the Job model
    job_fields = [field.name for field in Job._meta.fields]

    # Write the field names as headers
    writer.writerow(job_fields)

    jobs = Job.objects.all()
    for job in jobs:
        # Create a list of values for each field in the same order as the headers
        job_data = [getattr(job, field) for field in job_fields]

        # Write the data to the CSV row
        writer.writerow(job_data)

    return response

import csv
from django.http import HttpResponse
from django.shortcuts import render
from jobs.models import JobSubmission

def export_job_submissions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="job_submissions.csv"'

    writer = csv.writer(response)

    # Get all field names for the JobSubmission model
    submission_fields = [field.name for field in JobSubmission._meta.fields]

    # Write the field names as headers
    writer.writerow(submission_fields)

    submissions = JobSubmission.objects.all()
    for submission in submissions:
        # Create a list of values for each field in the same order as the headers
        submission_data = [getattr(submission, field) for field in submission_fields]

        # Write the data to the CSV row
        writer.writerow(submission_data)

    return response