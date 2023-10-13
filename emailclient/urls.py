from django.urls import path
from . import views

urlpatterns = [
    path('emailclient/', views.emailclient, name='emailclient'),
]