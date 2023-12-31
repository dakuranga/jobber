from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidate
from jobs.models import JobSubmission
from .forms import CandidateForm
from django.db.models import Q 
from django.core.paginator import Paginator
from django.utils import timezone 
from datetime import datetime, timedelta
from user_management.models import CustomUser


def candidates(request):
    query = request.GET.get('q', '')
    recruiter = request.GET.get('recruiter', '')

    date_range = request.GET.get('date_range', '')
    source_filter = request.GET.get('source_filter', '') 

    candidates = Candidate.objects.all()

    if query:
        candidates = candidates.filter(Q(name__icontains=query) | Q(email__icontains=query))

    if date_range:
        try:
            start_date_str, end_date_str = date_range.split(' to ')
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
            
            start_date = timezone.make_aware(start_date)
            end_date = timezone.make_aware(end_date)

            candidates = candidates.filter(created_at__range=(start_date, end_date))
        except ValueError:
            pass  # Handle the error

    if recruiter:
        candidates = candidates.filter(user__name__icontains=recruiter)

    if source_filter:
        if source_filter == 'sourced':
            candidates = candidates.filter(source='recruiter')
        elif source_filter == 'incoming':
            candidates = candidates.filter(source='application')

    candidates = candidates.order_by('-created_at')



    paginator = Paginator(candidates, 20)
    page_number = request.GET.get('page')
    candidates_page = paginator.get_page(page_number)

    context = {
        'candidates': candidates_page,
        'search_query': query,
        'date_range': date_range,
        'recruiter': recruiter,
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
            candidate.source = 'recruiter'

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
        if not form.is_valid():
                print(form.errors)

        if form.is_valid():
            form.instance.source = 'recruiter' 
            form.instance.user = request.user
            form.save()
            print("Form saved successfully!")
            return redirect('candidates')
        else:
            print("Form is invalid!") 
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
from jobs.models import JobSubmission
from jobs.models import JobSubmissionHistory


def update_submission_stage(request, submission_id):
    submission = get_object_or_404(JobSubmission, id=submission_id)

    if request.method == "POST":
        form = UpdateStageForm(request.POST, instance=submission)
        if form.is_valid():
            current_stage = form.cleaned_data['stage']
            if current_stage == "Client Submission":
                submission.date_client_submitted = timezone.now()
            submission.save()

            if submission.stage != current_stage:
                # Create a JobSubmissionHistory record
                JobSubmissionHistory.objects.create(
                    job_submission=submission,
                    stage=current_stage,
                    changed_at=timezone.now()
                )

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
            successful_imports = 0
            existing_candidates = 0

            # Get the list of uploaded CVs
            for cv_file in request.FILES.getlist('cv'):
                print("Processing CV:", cv_file.name)

                parsed_data = extract_data_from_cv(cv_file)
                print("Parsed data:", parsed_data)
                email = parsed_data.get("email", "")
                existing_candidate = Candidate.objects.filter(email=email).first()

                if existing_candidate:
                    existing_candidates += 1
                    continue 

                candidate = Candidate()  # Create a new instance here
                candidate.name = parsed_data.get("name", "")
                candidate.email = email
                candidate.phone = parsed_data.get("phone", "")
                candidate.cv = cv_file
                candidate.user = request.user
                candidate.source = 'recruiter'

                candidate.save()

                successful_imports += 1
            
            messages.success(
                request,
                f"{successful_imports} CV(s) imported successfully. {existing_candidates} already exist."
            )

            return redirect('candidates')
    else:
        form = CVImportForm()
    return render(request, 'import_candidate.html', {'form': form})


from datetime import datetime
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from clients.models import Client
from jobs.models import JobSubmission
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from django.forms.models import model_to_dict



def display_submissions(request):
    submissions = JobSubmission.objects.all().order_by('-date_submitted')
    query = request.GET.get('q', '')
    date_range = request.GET.get('date_range', '')
    recruiter = request.GET.get('recruiter', '')
    selected_client = request.GET.get('client', '')
    stage = request.GET.get('stage', '') 

    clients = Client.objects.all()  # Get all clients

    if selected_client:
        submissions = submissions.filter(job__client__id=selected_client)  # Adjust the field names as needed

    if stage:
        submissions = submissions.filter(stage=stage)

    stages = JobSubmission.STAGE_CHOICES  # Get the stage choices

    if query:
        submissions = submissions.filter(
            Q(candidate__name__icontains=query) |
            Q(job__job_title__icontains=query) |
            Q(job__client__name__icontains=query)
        )

    if date_range:
        try:
            start_date_str, end_date_str = date_range.split(' to ')
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            submissions = submissions.filter(date_submitted__range=(start_date, end_date))
        except ValueError:
            pass

    if recruiter:
        submissions = submissions.filter(candidate__user__name__icontains=recruiter)

    submissions_list = [{
    'Date Submitted': sub.date_submitted.strftime('%d-%m-%Y'),
    'Candidate': sub.candidate.name,
    'Resume': request.build_absolute_uri(sub.candidate.cv.url) if sub.candidate.cv else '',  # Add this line
    'Job Title': sub.job.job_title,
    'Email': sub.candidate.email,
    'Phone': sub.candidate.phone,
    'Client': sub.job.client.name,
    'Serving Notice': sub.candidate.serving_notice_period,
    'Availability': sub.candidate.expected_joining_date,
    'ECTC': str(sub.candidate.expected_ctc), 
    'CTC': str(sub.candidate.current_ctc), 
    'Stage': sub.stage,  
    'Location': sub.candidate.location,
    'Notes': sub.candidate.recruiter_notes,
    'Recruiter': sub.user.name,
    # add other fields as needed
} for sub in submissions]

    request.session['submissions_data'] = submissions_list

    context = {
        'submissions': submissions,
        'search_query': query,
        'date_range': date_range,
        'recruiter': recruiter,
        'clients': clients,  # Pass the clients to the context
        'selected_client': selected_client,
        'stage': stage,   # Add selected stage to the context
        'stages': stages
    }

    return render(request, 'submissions.html', context)


from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime

@login_required
@user_passes_test(lambda u: u.is_superuser)
def export_submissions(request):
    # Get the submissions data from the session
    submissions_data = request.session.get('submissions_data', [])

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(submissions_data)

    # Check if there is data to export
    if not df.empty:
        # Optional: Format the DataFrame as needed before exporting

        # Write DataFrame to Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Submissions')
            
            # Get the xlsxwriter workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Submissions']

        excel_content = output.getvalue()

        # Prepare the response with the Excel file
        response = HttpResponse(
            excel_content,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        current_date = datetime.now().strftime("%Y-%m-%d")
        response['Content-Disposition'] = f'attachment; filename={current_date}_Submissions.xlsx'

        return response
    else:
        messages.error(request, "There is no data to export.")
        return redirect('display_submissions')