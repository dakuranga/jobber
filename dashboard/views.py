from django.shortcuts import render
from candidates.models import Candidate
from jobs.models import JobSubmission, Job
from user_management.models import CustomUser
from django.utils import timezone
from django.db.models import Count
from django.db.models import Q
from datetime import date, timedelta
from interviews.models import Interview
import datetime


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


# masterdashboard/views.py

from django.shortcuts import render
from django.db.models import Count
from candidates.models import Candidate
from jobs.models import JobSubmission, JobSubmissionHistory
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test


def master_dashboard(request, date_filter=None):
    # Get the date range from the query parameters (if provided)
    

    start_date = None
    end_date = None
    date_range_str = None 

    if date_filter == 'this_month':
        today = datetime.today().date()
        start_date = today.replace(day=1)
        end_date = today
        date_range_str = f"{start_date} to {end_date}"

    elif date_filter is None:

        date_range_str = request.GET.get('date_range')
        # Convert the date strings to datetime objects
        if date_range_str:
            date_strings = date_range_str.split(' to ')

            start_date_str = date_strings[0]
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

            if len(date_strings) > 1:
                end_date_str = date_strings[1]
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()



    # Filter candidates by date range if available
    candidates = Candidate.objects.all()

    if start_date and end_date:
        candidates = candidates.filter(created_at__date__range=(start_date, end_date))
    elif start_date:
        candidates = candidates.filter(created_at__date__gte=start_date)
    elif end_date:
        candidates = candidates.filter(created_at__date__lte=end_date)

    # Count sourced candidates for each user
    user_counts = candidates.values('user__name').annotate(
        sourced_count=Count('id')
    ).order_by('user__name')

    # Count internal submissions for each user
    internal_submissions = JobSubmission.objects.all()

    if start_date and end_date:
        internal_submissions = internal_submissions.filter(date_submitted__date__range=(start_date, end_date))
    elif start_date:
        internal_submissions = internal_submissions.filter(date_submitted__date__gte=start_date)
    elif end_date:
        internal_submissions = internal_submissions.filter(date_submitted__date__lte=end_date)

    internal_submissions_counts = internal_submissions.values('candidate__user__name').annotate(
        internal_submissions_count=Count('id')
    )

    # Include the count of QC Rejects and External Submissions, ensuring that these are distinct counts
    qc_rejects = JobSubmission.objects.filter(stage='QC Reject').distinct()
    external_submissions = JobSubmission.objects.filter(stage__in=['Client Submission', 'L1 Interview', 'L2 Interview', 'L3 Interview', 'Interview Reject', 'Shortlisted', 'Joined']).distinct()

    if start_date and end_date:
        qc_rejects = qc_rejects.filter(stage_changed_date__date__range=(start_date, end_date))
        external_submissions = external_submissions.filter(stage_changed_date__date__range=(start_date, end_date))
    elif start_date:
        qc_rejects = qc_rejects.filter(stage_changed_date__date__gte=start_date)
        external_submissions = external_submissions.filter(stage_changed_date__date__gte=start_date)
    elif end_date:
        qc_rejects = qc_rejects.filter(stage_changed_date__date__lte=end_date)
        external_submissions = external_submissions.filter(stage_changed_date__date__lte=end_date)

    qc_rejects_counts = qc_rejects.values('candidate__user__name').annotate(
        qc_reject_count=Count('id')
    )

    external_submissions_counts = external_submissions.values('candidate__user__name').annotate(
        external_submissions_count=Count('id')
    )

    joined_candidates = JobSubmission.objects.filter(stage='Joined').distinct()
    shortlisted_candidates = JobSubmission.objects.filter(stage='Shortlisted').distinct()
    interview_reject_candidates = JobSubmission.objects.filter(stage='Interview Reject').distinct()
    interviews = JobSubmission.objects.filter(stage__in=['L1 Interview', 'L2 Interview', 'L3 Interview', 'Interview Reject', 'Shortlisted', 'Joined']).distinct()


    if start_date and end_date:
        joined_candidates = joined_candidates.filter(stage_changed_date__date__range=(start_date, end_date))
        shortlisted_candidates = shortlisted_candidates.filter(stage_changed_date__date__range=(start_date, end_date))
        interview_reject_candidates = interview_reject_candidates.filter(stage_changed_date__date__range=(start_date, end_date))
        interviews = interviews.filter(stage_changed_date__date__range=(start_date, end_date))
    elif start_date:
        joined_candidates = joined_candidates.filter(stage_changed_date__date__gte=start_date)
        shortlisted_candidates = shortlisted_candidates.filter(stage_changed_date__date__gte=start_date)
        interview_reject_candidates = interview_reject_candidates.filter(stage_changed_date__date__gte=start_date)
        interviews = interviews.filter(stage_changed_date__date__gte=start_date)
    elif end_date:
        joined_candidates = joined_candidates.filter(stage_changed_date__date__lte=end_date)
        shortlisted_candidates = shortlisted_candidates.filter(stage_changed_date__date__lte=end_date)
        interview_reject_candidates = interview_reject_candidates.filter(stage_changed_date__date__lte=end_date)
        interviews = interviews.filter(stage_changed_date__date__lte=end_date)


    joined_candidates_counts = joined_candidates.values('candidate__user__name').annotate(
        joined_count=Count('id')
    )

    shortlisted_candidates_counts = shortlisted_candidates.values('candidate__user__name').annotate(
        shortlisted_count=Count('id')
    )

    interview_reject_candidates_counts = interview_reject_candidates.values('candidate__user__name').annotate(
        interview_reject_count=Count('id')
    )

    interviews_counts = interviews.values('candidate__user__name').annotate(        
        interviews_count=Count('id')
    )



    # Merge the counts into the user_counts queryset
    for user_count in user_counts:
        user_name = user_count['user__name']

        user_internal_submissions = next((item for item in internal_submissions_counts if item["candidate__user__name"] == user_name), None)
        user_qc_rejects = next((item for item in qc_rejects_counts if item["candidate__user__name"] == user_name), None)
        user_external_submissions = next((item for item in external_submissions_counts if item["candidate__user__name"] == user_name), None)
        user_interviews = next((item for item in interviews_counts if item["candidate__user__name"] == user_name), None)
        user_shortlisted = next((item for item in shortlisted_candidates_counts if item["candidate__user__name"] == user_name), None)
        user_interview_rejected = next((item for item in interview_reject_candidates_counts if item["candidate__user__name"] == user_name), None)
        user_joined = next((item for item in joined_candidates_counts if item["candidate__user__name"] == user_name), None)
        


        user_count['internal_submissions_count'] = user_internal_submissions['internal_submissions_count'] if user_internal_submissions else 0
        user_count['qc_reject_count'] = user_qc_rejects['qc_reject_count'] if user_qc_rejects else 0
        user_count['external_submissions_count'] = user_external_submissions['external_submissions_count'] if user_external_submissions else 0
        user_count['interviews_count'] = user_interviews['interviews_count'] if user_interviews else 0
        
        user_count['shortlisted_count'] = user_shortlisted['shortlisted_count'] if user_shortlisted else 0
        user_count['interview_reject_count'] = user_interview_rejected['interview_reject_count'] if user_interview_rejected else 0
        user_count['joined_count'] = user_joined['joined_count'] if user_joined else 0
        
        

    request.session['user_counts'] = list(user_counts)

    context = {
        'user_counts': user_counts,
        'date_filter': date_filter, 
        'date_range': date_range_str,

    }

    return render(request, 'master_dashboard.html', context)



# New view to export the data as an Excel file
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from candidates.models import Candidate
from jobs.models import JobSubmission
from datetime import datetime
import pandas as pd
from io import BytesIO
from django.shortcuts import redirect
from django.contrib import messages

@login_required
@user_passes_test(lambda u: u.is_superuser)
def export_custom_report(request):
    # Get the data from session
    user_counts = request.session.get('user_counts', [])

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(user_counts)

    # Check if there is data to export
    if not df.empty:
        
        # Rename the columns based on the provided mapping
        df.rename(columns={
            'user__name': 'Name',
            'sourced_count': '# Sourced',
            'internal_submissions_count': '# Internal Subs',
            'qc_reject_count': '# QC Rejects',
            'external_submissions_count': '# Client Subs',
            'interviews_count': '# Interviews Set',
            'shortlisted_count': '# Shortlisted',
            'interview_reject_count': '# Rejected In Interview',
            'joined_count': '# Joined'
        }, inplace=True)

        # Write DataFrame to Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Report')
            
            # Get the xlsxwriter workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Report']
            
            # Iterate over the columns and set the column width based on the max length in each column
            for idx, col in enumerate(df.columns):
                # Find the max length in each column (+2 to make it a bit wider for clearer visibility)
                max_len = max(df[col].astype(str).apply(len).max(), len(str(col))) + 2
                worksheet.set_column(idx, idx, max_len)  # Set column width

        excel_content = output.getvalue()

        # Prepare the response with the Excel file
        response = HttpResponse(
            excel_content,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        current_date = datetime.now().strftime("%Y-%m-%d")
        response['Content-Disposition'] = f'attachment; filename={current_date}_CustomReport.xlsx'

        return response
    else:
        messages.error(request, "There is no data to export.")
        return redirect('master_dashboard')


