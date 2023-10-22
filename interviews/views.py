from django.shortcuts import render, redirect
from .models import Interview
from jobs.models import JobSubmission
from .forms import InterviewDetailsForm
from django.shortcuts import get_list_or_404, get_object_or_404
import datetime
from django.db.models import Q
from clients.models import Client



def interviews(request):
    interviews = Interview.objects.all()
    query = request.GET.get('q', '')  # Get the search query from the URL parameter 'q' (default to empty string)
    recruiter_filter = request.GET.get('recruiter', '')  
    client_filter = request.GET.get('client', '')

    if query:
        interviews = interviews.filter(
        Q(submission__candidate__name__icontains=query) |   # Assuming candidate's name is a field in another model linked by ForeignKey
        Q(submission__job__job_title__icontains=query)   # Assuming job_title is a field in another model linked by ForeignKey
        )
    
    if recruiter_filter:
        interviews = interviews.filter(user__name__icontains=recruiter_filter)
        
    # Apply client filter if it exists
    if client_filter:
        interviews = interviews.filter(submission__job__client__id=client_filter)
    
    clients = Client.objects.all() 
    
    context = {
        'interviews': interviews,
        'search_query': query,
        'recruiter_filter': recruiter_filter,
        'client_filter': client_filter,
        'clients': clients 
    }
    return render(request, 'interviews.html', context)


from interviews.models import InterviewStageChange  # Import at the top of your views.py

def interview_details_form(request, submission_id):
    submission = get_object_or_404(JobSubmission, id=submission_id)
    if request.method == 'POST':
        form = InterviewDetailsForm(request.POST)
        if form.is_valid():

            # Create the Interview record
            interview = Interview.objects.create(
                submission=submission,
                user=submission.user,
                stage=submission.stage,
                mode=form.cleaned_data['mode'],
                interviewer=form.cleaned_data['interviewer'],
                interview_date=form.cleaned_data['interview_date'],
                interview_time=form.cleaned_data['interview_time'],
                feedback="Pending",

            )

            # Create a record for the stage change (InterviewStageChange entry)
            InterviewStageChange.objects.create(interview=interview, stage=submission.stage)

            # Redirect back to the job details page
            return redirect('job_details', job_id=submission.job.id)

    else:
        form = InterviewDetailsForm()

    return render(request, 'interview_details_form.html', {'form': form, 'submission': submission})




