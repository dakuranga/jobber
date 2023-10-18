from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidate
from .forms import CandidateForm
from django.db.models import Q 
from django.core.paginator import Paginator
from django.utils import timezone 
from jobs.models import JobSubmission


def candidates(request):
    
    # Fetch and filter the candidates first.
    query = request.GET.get('q', '')  # Get the search query from the URL parameter 'q' (default to empty string)

    # If a query exists, filter candidates by name with partial matches using Q objects
    if query:
        candidates = Candidate.objects.filter(
            Q(name__icontains=query)  # Case-insensitive partial match on 'name'
        ).order_by('-created_at')
    else:
        candidates = Candidate.objects.order_by('-created_at')
        
    # Now paginate the filtered candidates.
    paginator = Paginator(candidates, 20 )  # Show 10 candidates per page (you can change this number)
    page_number = request.GET.get('page')
    candidates_page = paginator.get_page(page_number)

    context = {
        'candidates': candidates_page,  # You should pass the paginated results to the context.
        'search_query': query,  # Pass the search query back to the template
    }
    return render(request, 'candidates.html', context)

from django.contrib import messages
def add_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']  # Get email from the form
            existing_candidate = Candidate.objects.filter(email=email).first()

            if existing_candidate:
                messages.warning(request, f"Candidate with email {email} already exists.")
    # Render the form again with the filled data to give user feedback
                return render(request, 'add_candidate.html', {'form': form})

            

            candidate = form.save(commit=False)
            candidate.user = request.user
            candidate.save()
            return redirect('candidates')
    else:
        form = CandidateForm()
    return render(request, 'add_candidate.html', {'form': form})






def edit_candidate(request, candidate_id):
    form = None
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('candidates')
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'edit_candidate.html', {'form': form})

from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_candidate(request):
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        candidate = get_object_or_404(Candidate, id=candidate_id)
        candidate.delete()
        return redirect('candidates')

from django.shortcuts import render, get_object_or_404
from .models import Candidate

def candidate_details(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    context = {'candidate': candidate}
    return render(request, 'candidate_details.html', context)

from interviews.models import Interview
from django.shortcuts import render, redirect
from .forms import JobSubmissionForm
from candidates.models import Candidate
from jobs.models import JobSubmission
from django.contrib import messages

def submit_candidate_to_job(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    
    if request.method == 'POST':
        form = JobSubmissionForm(request.POST)
        if form.is_valid():
            # Check for previous submission
            previous_submission = JobSubmission.objects.filter(job=form.cleaned_data['job'], candidate=candidate).first()
            
            if previous_submission:
                # Notify user of previous submission and do not save the new submission
                messages.warning(request, f'This candidate was already submitted to this job on {previous_submission.date_submitted.strftime("%Y-%m-%d")}.')
                return redirect('candidates')
            
            else:
                job_submission = form.save(commit=False)
                job_submission.candidate = candidate
                job_submission.user = request.user 
                if not JobSubmission.objects.filter(candidate=candidate).exists():job_submission.stage = 'Internal'
                job_submission.stage_changed_date = timezone.now().date() 
                job_submission.save()
                messages.success(request, 'Candidate successfully submitted to the job!')
                return redirect('candidates')

    else:
        form = JobSubmissionForm()

    return render(request, 'submit_candidate_to_job.html', {'form': form, 'candidate': candidate})

from .forms import CandidateSubmissionForm
from jobs.models import Job

def submit_candidate_for_job(request, job_id):
    job = Job.objects.get(id=job_id)
    query = request.GET.get('search', '')
    candidates = Candidate.objects.filter(name__icontains=query).order_by('name')  # Assuming the name is the search criterion
    
    # Implement pagination
    paginator = Paginator(candidates, 10)  # Show 10 candidates per page
    page = request.GET.get('page')
    candidates = paginator.get_page(page)

    if request.method == 'POST':
        form = CandidateSubmissionForm(request.POST)
        if form.is_valid():
            candidate = form.cleaned_data['candidate']
            
            # Check for previous submission
            previous_submission = JobSubmission.objects.filter(job=job, candidate=candidate).first()
            
            if previous_submission:
                messages.warning(request, f'This candidate was already submitted to this job on {previous_submission.date_submitted.strftime("%Y-%m-%d")}.')
                return redirect('jobs')  # redirect to the job listing page, adjust if needed
            
            else:
                job_submission = form.save(commit=False)
                job_submission.job = job
                job_submission.user = request.user
                if not JobSubmission.objects.filter(candidate=candidate).exists():job_submission.stage = 'Internal'
                job_submission.stage_changed_date = timezone.now().date() 
                job_submission.save()
                messages.success(request, 'Candidate successfully submitted to the job!')
                return redirect('jobs')  # again, adjust the redirect as necessary

    else:
        form = CandidateSubmissionForm()

    return render(request, 'submit_candidate_for_job.html', {'candidates': candidates, 'job': job})

from django.shortcuts import render, get_object_or_404, redirect
from .forms import UpdateStageForm  
from interviews.models import Interview
from django.utils import timezone
from django.db import transaction
from interviews.models import Interview

def update_submission_stage(request, submission_id):
    submission = get_object_or_404(JobSubmission, id=submission_id)

    if request.method == "POST":
        form = UpdateStageForm(request.POST, instance=submission)
        if form.is_valid():
            current_stage = form.cleaned_data['stage']
            if current_stage == "Client Submission":
                submission.date_client_submitted = timezone.now()
            submission.save()

            # Update interview records, if necessary
            interview_stages = ['L1 Interview', 'L2 Interview', 'L3 Interview']
            if current_stage in interview_stages:
                return redirect('interview_details_form', submission_id=submission.id)
            else:
                submission.stage_changed_date = timezone.localtime(timezone.now()).date()
                submission.save()
                return redirect('job_details', job_id=submission.job.id)

    else:  # This else block will handle the GET request
        form = UpdateStageForm(instance=submission)

    return render(request, 'change_stage.html', {'form': form, 'submission': submission})


from .forms import CVImportForm
from .data_extractors import extract_data_from_cv
from django.contrib import messages

def import_candidate(request):
    if request.method == 'POST':
        form = CVImportForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the list of uploaded CVs
            for cv_file in request.FILES.getlist('cv'):
                candidate = form.save(commit=False)
                parsed_data = extract_data_from_cv(cv_file)
                
                email = parsed_data.get("email", "")
                existing_candidate = Candidate.objects.filter(email=email).first()

                if existing_candidate:
                    messages.warning(request, f"Candidate with email {email} already exists.")
                    continue  # Skip this CV and move to the next one
                
                candidate.name = parsed_data.get("name", "")
                candidate.email = email
                candidate.phone = parsed_data.get("phone", "")
                candidate.cv = cv_file
                candidate.user = request.user
                candidate.save()

            return redirect('candidates')
    else:
        form = CVImportForm()
    return render(request, 'import_candidate.html', {'form': form})

from datetime import datetime
from django.http import JsonResponse

from django.core.paginator import Paginator

from django.db.models import Q

def display_submissions(request):
    submissions = JobSubmission.objects.all().order_by('-date_submitted')
    query = request.GET.get('q', '')  # Get the search query from the URL parameter 'q' (default to empty string)
    
    # If a query exists, filter candidates by name with partial matches using Q objects
    if query:
        submissions = submissions.filter(
        Q(candidate__name__icontains=query) |   # Assuming candidate's name is a field in another model linked by ForeignKey
        Q(job__job_title__icontains=query) |    # Assuming job_title is a field in another model linked by ForeignKey
        Q(job__client__name__icontains=query)   # Assuming client is a field in another model linked by ForeignKey and has a 'name' attribute
    ).order_by('-date_submitted')

    context = {
        'submissions': submissions,  # You should pass the paginated results to the context.
        'search_query': query,  # Pass the search query back to the template
    }

    return render(request, 'submissions.html', context)

