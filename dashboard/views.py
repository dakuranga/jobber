from django.shortcuts import render
from candidates.models import Candidate
from jobs.models import JobSubmission
from user_management.models import CustomUser
from django.utils import timezone
from django.db.models import Count
from jobs.models import Job
from django.db.models import Q 
import json
from datetime import date, timedelta
from interviews.models import Interview


def get_candidate_count_for_user_today(user, today):
    return Candidate.objects.filter(
        user=user,
        created_at__date__day=today.day,
        created_at__date__month=today.month,
        created_at__date__year=today.year
    ).count()

def get_internal_submission_count_for_user_today(user, today):
    return JobSubmission.objects.filter(
        user=user,
        date_submitted__date__day=today.day,
        date_submitted__date__month=today.month,
        date_submitted__date__year=today.year,
    ).count()

def get_client_submission_count_for_user_today(user, today):
    return JobSubmission.objects.filter(
        user=user,
        date_client_submitted__date__day=today.day,
        date_client_submitted__date__month=today.month,
        date_client_submitted__date__year=today.year,
    ).count()

def get_qc_reject_count_for_user_today(user, today):
    return JobSubmission.objects.filter(
        user=user,
        stage='QC Reject',
        date_submitted__date__day=today.day,
        date_submitted__date__month=today.month,
        date_submitted__date__year=today.year
    ).count()

from interviews.models import InterviewStageChange
def get_interview_count_for_user_today(user, today, stage):
    return InterviewStageChange.objects.filter(
        interview__user=user,
        stage=stage,
        changed_date__date=today
    ).count()

def get_shortlisted_count_for_user_today(user, today):
    return JobSubmission.objects.filter(
        user=user,
        stage='Shortlisted',
        stage_changed_date__day=today.day,
        stage_changed_date__month=today.month,
        stage_changed_date__year=today.year
    ).count()

def get_joined_count_for_user_today(user, today):
    return JobSubmission.objects.filter(
        user=user,
        stage='Joined',
        stage_changed_date__day=today.day,
        stage_changed_date__month=today.month,
        stage_changed_date__year=today.year
    ).count()

def get_candidate_count_for_job_today(job, today):
    return Candidate.objects.filter(
        job=job,
        created_at__date__day=today.day,
        created_at__date__month=today.month,
        created_at__date__year=today.year
    ).count()

def get_interview_count_for_job_today(job, today, stage):
    return InterviewStageChange.objects.filter(
        interview__submission__job=job,
        stage=stage,
        changed_date__date=today
    ).count()

def dashboard(request):
    today = timezone.localdate()
    users = CustomUser.objects.all()
    total_open_requirements = Job.objects.filter(job_status='Open').count()
    total_high_priority_requirements = Job.objects.filter(job_status='Open', job_priority='High').count()


    user_data = []
    for user in users:
        user_data.append({
            'user': user,
            'sourced_count': get_candidate_count_for_user_today(user, today),
            'internal_submissions': get_internal_submission_count_for_user_today(user, today),
            'client_submissions': get_client_submission_count_for_user_today(user, today),
            'l1_interview_count': get_interview_count_for_user_today(user, today, 'L1 Interview'),
            'l2_interview_count': get_interview_count_for_user_today(user, today, 'L2 Interview'),
            'l3_interview_count': get_interview_count_for_user_today(user, today, 'L3 Interview'),
            'qc_reject_count': get_qc_reject_count_for_user_today(user, today),
            'shortlisted_count': get_shortlisted_count_for_user_today(user, today),
            'joined_count': get_joined_count_for_user_today(user, today),
        })

    total_counts = {
        'sourced_count': 0,
        'internal_submissions': 0,
        'qc_reject_count': 0,
        'client_submissions': 0,
        'l1_interview_count': 0,
        'l2_interview_count': 0,
        'l3_interview_count': 0,
        'shortlisted_count': 0,
        'joined_count': 0
    }
    
    for data in user_data:
        for key, value in data.items():
            if key in total_counts:
                total_counts[key] += value


    from datetime import date

    upcoming_interviews = Interview.objects.filter(interview_date__gte=date.today()).order_by('interview_date')

    jobs = Job.objects.filter(job_status="Open")
    job_data = []
    for job in jobs:
        sourced_count = get_candidate_count_for_job_today(job, today)
        internal_count = JobSubmission.objects.filter(job=job, date_submitted__date=today).count()
        qc_reject_count = JobSubmission.objects.filter(job=job, stage="QC Reject", stage_changed_date__date=today).count()
        client_submission_count = JobSubmission.objects.filter(job=job, date_client_submitted__date=today).count()
        l1_interview_count = get_interview_count_for_job_today(job, today, 'L1 Interview')
        l2_interview_count = get_interview_count_for_job_today(job, today, 'L2 Interview')
        l3_interview_count = get_interview_count_for_job_today(job, today, 'L3 Interview')
        shortlisted_count = JobSubmission.objects.filter(job=job, stage='Shortlisted', stage_changed_date__date=today).count()
        joined_count = JobSubmission.objects.filter(job=job, stage='Joined', stage_changed_date__date=today).count()



        job_data.append({
            "job_title": job.job_title,
            "sourced_count": sourced_count,
            "internal_count": internal_count,
            "qc_reject_count": qc_reject_count,
            "client_submission_count": client_submission_count,
            "l1_interview_count": l1_interview_count,
            "l2_interview_count": l2_interview_count,
            "l3_interview_count": l3_interview_count,
            "shortlisted_count": shortlisted_count,
            "joined_count": joined_count,
        })

    context = {
        'users': users,
        'total_open_requirements': total_open_requirements,
        'total_high_priority_requirements': total_high_priority_requirements,

        'get_candidate_count_for_user_today': get_candidate_count_for_user_today,
        'get_internal_submission_count_for_user_today': get_internal_submission_count_for_user_today,
        'get_client_submission_count_for_user_today': get_client_submission_count_for_user_today,
        'today': today,
        'user_data': user_data,

        'total_counts': total_counts,
        'upcoming_interviews': upcoming_interviews,
        "job_data": job_data,

    }
    return render(request, 'dashboard.html', context)


