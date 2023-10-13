from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse  # Add this import statement
from .models import Job, Client
from .forms import JobForm, JobFilterForm
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test

def jobs(request):
    jobs = Job.objects.all().order_by('-date_added')
    form = JobFilterForm(request.GET)

    if form.is_valid():
        status_filter = form.cleaned_data['job_status']
        priority_filter = form.cleaned_data['job_priority']
        client_filter = form.cleaned_data['client']

        if status_filter:
            jobs = jobs.filter(job_status=status_filter)
        if priority_filter:
            jobs = jobs.filter(job_priority=priority_filter)
        if client_filter:
            jobs = jobs.filter(client=client_filter)
    else:
        form = JobFilterForm()
        jobs = Job.objects.all()
    
    
    # Paginate the jobs
    paginator = Paginator(jobs, 8)  # Show 10 jobs per page (you can change this number)
    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)

    context = {
        'jobs': jobs_page,  # Use the paginated jobs queryset
        'filter_form': form,
    }
    return render(request, 'jobs.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            return redirect('jobs')
    else:
        form = JobForm(instance=job)
    return render(request, 'edit_job.html', {'form': form, 'job': job})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_job(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        job.delete()
        return redirect('jobs')
    else:
        return redirect('jobs')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)  # add request.FILES here
        if form.is_valid():
            form.save()
            return redirect('jobs')
    else:
        form = JobForm()
    context = {'form': form}
    return render(request, 'add_job.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Job, JobSubmission
from candidates.models import Candidate  
from django.utils import timezone

def job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    all_submissions = JobSubmission.objects.filter(job=job)
    total_subs = all_submissions.count()
    
    # Count of Client Submissions
    client_submission_stages = [
    'Client Submission', 
    'L1 Interview', 
    'L2 Interview', 
    'L3 Interview', 
    'Shortlisted', 
    'Interview Reject', 
    'Joined'
]
    

    client_submissions = all_submissions.filter(stage__in=client_submission_stages).count()

    interview_stages = [
    'L1 Interview', 
    'L2 Interview', 
    'L3 Interview', 
    'Shortlisted', 
    'Interview Reject', 
    'Joined'
]
    # Count of Total Interviews
    total_interviews = all_submissions.filter(stage__in=interview_stages).values('candidate').distinct().count()
    
    # Count of Total shortlist
    shortlist_stages = [

    'Shortlisted', 
    'Joined'
    ]

    total_shortlist = all_submissions.filter(stage__in=shortlist_stages).values('candidate').distinct().count()

    # Count of Total Joining
    joinings_stages = [
    'Joined'
    ]

    total_joinings = all_submissions.filter(stage__in=joinings_stages).values('candidate').distinct().count()

    qc_rejects = all_submissions.filter(stage='QC Reject').count()
    interview_rejects = all_submissions.filter(stage='Interview Reject').count()

    stages = {choice[0]: [] for choice in JobSubmission.STAGE_CHOICES}
    
    for submission in all_submissions:
        stages[submission.stage].append({
            'candidate': submission.candidate,
            'submission_id': submission.id
        })

    days_open = (timezone.now() - job.date_added).days + 1 
    context = {
        'job': job,
        'days_open': days_open,
        'stages': stages,
        'total_subs': total_subs,
        'client_submissions': client_submissions,  
        'total_interviews': total_interviews,       
        'total_shortlist': total_shortlist,
        'total_joinings': total_joinings,
        'qc_rejects': qc_rejects,
        'interview_rejects': interview_rejects
    }
    
    return render(request, 'job_details.html', context)