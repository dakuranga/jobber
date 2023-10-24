# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('publish_job/<int:job_id>/', views.publish_job, name='publish_job'),
    path('unpublish_job/<int:job_id>/', views.unpublish_job, name='unpublish_job'), 
    path('jobs-at-linksoft/', views.job_listing, name='job_listing'),
    path('jobs-at-linksoft/<int:job_id>/apply/', views.job_detail_and_apply, name='job_detail_and_apply'),



]
