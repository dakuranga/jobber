from django.urls import path
from . import views

urlpatterns = [
    # ... other url patterns
    path('interviews/', views.interviews, name='interviews'),
    path('interview_details_form/<int:submission_id>/', views.interview_details_form, name='interview_details_form')
]
