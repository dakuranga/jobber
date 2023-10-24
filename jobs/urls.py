from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/add/', views.add_job, name='add_job'),
    path('jobs/edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('jobs/delete/', views.delete_job, name='delete_job'),
    path('jobs/details/<int:job_id>/', views.job_details, name='job_details'),
    path('jobs/details/<int:job_id>/export-excel/', views.export_job_details_to_excel, name='export_job_details_to_excel'),
    path('jobs/<int:job_id>/', views.view_job, name='view_job'),





]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
