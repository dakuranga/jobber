from django.urls import path, include
from . import views
from .views import revoke_google_integration


urlpatterns = [
    path('emailclient/', views.emailclient, name='emailclient'),

    path('auth/gmail/', views.auth_gmail, name='auth_gmail'),
    path('auth/callback/', views.auth_callback, name='auth_callback'),

    path('revoke-google-oauth/', revoke_google_integration, name='revoke_google_oauth'),





]