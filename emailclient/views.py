from django.shortcuts import render

def emailclient(request):
    return render(request, 'emailclient.html')

from django.shortcuts import render, redirect
from user_management.models import CustomUser
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.urls import reverse
from google_auth_oauthlib.flow import InstalledAppFlow

def auth_gmail(request):
    redirect_uri = "http://127.0.0.1:8000/auth/callback/" 
    flow = InstalledAppFlow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
                "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                "redirect_uris": [redirect_uri],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
            }
        },
        [
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email"
    ]
    )
    authorization_url, _ = flow.authorization_url(
        access_type="offline", prompt="consent"
    )
    authorization_url += "&redirect_uri=" + redirect_uri
    return redirect(authorization_url)

from requests_oauthlib import OAuth2Session
from emailclient.models import UserEmail
from django.conf import settings
from django.shortcuts import redirect
from datetime import timedelta
from django.utils import timezone

def auth_callback(request):
    redirect_uri = "http://127.0.0.1:8000/auth/callback/"
    google = OAuth2Session(settings.GOOGLE_OAUTH2_CLIENT_ID, redirect_uri=redirect_uri)
    token = google.fetch_token(
        token_url="https://accounts.google.com/o/oauth2/token",
        authorization_response=request.build_absolute_uri(),
        client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET
    )
    expires_in = token.get('expires_in', 3600)  # Default to 1 hour if 'expires_in' is not present
    expiration_time = timezone.now() + timedelta(seconds=expires_in)
    user_email, created = UserEmail.objects.get_or_create(user=request.user)
    user_email.access_token = token['access_token']
    user_email.refresh_token = token.get('refresh_token')
    user_email.token_expiration = expiration_time
    user_email.save()
    return redirect('settings')

from datetime import datetime, timedelta
from django.http import HttpResponse
from django.conf import settings
from requests_oauthlib import OAuth2Session
from .models import UserEmail
from django.utils.timezone import now

def should_refresh_token(user_email):
    current_time = now()
    if user_email.token_expiration:
        return user_email.token_expiration - current_time < timedelta(minutes=5)
    return False

def refresh_access_token(user_email):
    if should_refresh_token(user_email):
        google = OAuth2Session(
            settings.GOOGLE_OAUTH2_CLIENT_ID,
            token={
                'access_token': user_email.access_token,
                'refresh_token': user_email.refresh_token,
                'token_type': 'Bearer',
                'expires_at': user_email.token_expiration.timestamp()
            }
        )
        token = google.refresh_token(
            token_url="https://accounts.google.com/o/oauth2/token",
            client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET
        )
        user_email.access_token = token['access_token']
        user_email.refresh_token = token.get('refresh_token', user_email.refresh_token)
        expires_in = token.get('expires_in', 3600)  
        user_email.token_expiration = datetime.utcnow() + timedelta(seconds=expires_in)
        user_email.save()

def check_and_refresh_token(request):
    user_email = UserEmail.objects.get(user=request.user)
    refresh_access_token(user_email)
    return user_email.access_token

from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import requests
from emailclient.models import UserEmail

@login_required
def revoke_google_integration(request):
    try:
        user_email = UserEmail.objects.get(user=request.user)  
        revoke_url = "https://oauth2.googleapis.com/revoke"
        params = {'token': user_email.access_token}  
        response = requests.post(revoke_url, params=params)

        if response.status_code == 200:
            user_email.delete()  
            messages.success(request, "Integration with Google removed and data cleaned up successfully!")
        else:
            messages.error(request, "Failed to revoke the Google integration. Please try again.")
    except UserEmail.DoesNotExist:
        messages.warning(request, "No Google integration found for this user.")

    return redirect('settings')  # Redirect back to the settings page


