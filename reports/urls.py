from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('reports/', views.reports, name='reports'),
    path('export-candidates/', views.export_candidates_page, name='export_candidates_page'),
    path('export-candidates-csv/', views.export_candidates_csv, name='export_candidates_csv'),
    path('export-candidates-zip/', views.export_candidates_zip, name='export_candidates_zip'),
    path('export-jobs-csv/', views.export_jobs_csv, name='export_jobs_csv'),
    path('export-job-submissions-csv/', views.export_job_submissions_csv, name='export_job_submissions_csv'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

