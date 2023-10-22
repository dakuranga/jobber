from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [ 
    path('candidates/', views.candidates, name='candidates'),
    path('candidates/add/', views.add_candidate, name='add_candidate'),
    path('candidates/edit/<int:candidate_id>/', views.edit_candidate, name='edit_candidate'),
    path('candidates/delete/', views.delete_candidate, name='delete_candidate'),
    path('candidates/<int:candidate_id>/', views.candidate_details, name='candidate_details'),
    path('submit-candidate/<int:candidate_id>/', views.submit_candidate_to_job, name='submit_candidate_to_job'),
    path('update_submission_stage/<int:submission_id>/', views.update_submission_stage, name='update_submission_stage'),
    path('candidates/import/', views.import_candidate, name='import_candidate'),
    path('submit_candidate_for_job/<int:job_id>/', views.submit_candidate_for_job, name='submit_candidate_for_job'),
    path('submissions/', views.display_submissions, name='display_submissions'),
    path('export_submissions/', views.export_submissions, name='export_submissions'),
 

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

