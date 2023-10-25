from django.shortcuts import render
from user_management.models import CustomUser  
from emailclient.models import UserEmail
from requests_oauthlib import OAuth2Session
from django.http import HttpResponse
from emailclient.views import check_and_refresh_token
from django.conf import settings as django_settings
from datetime import datetime



from emailclient.models import UserEmail

def settings(request):
    users = CustomUser.objects.all()  # Use your CustomUser model

    context = {
        'users': users,
    }

    return render(request, 'settings.html', context)

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

User = get_user_model()


def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('settings')  # Replace 'settings' with the name of your settings page URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_user.html', {'form': form})


# In views.py
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import redirect, get_object_or_404

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'edit_user.html', {'form': form, 'user': user})

# In views.py
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404

User = get_user_model()

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('settings')





