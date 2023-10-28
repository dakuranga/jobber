from django.shortcuts import render
from user_management.models import CustomUser  
from emailclient.models import UserEmail
from requests_oauthlib import OAuth2Session
from django.http import HttpResponse
from emailclient.views import check_and_refresh_token
from django.conf import settings as django_settings
from datetime import datetime
from .models import EmailSignature



from emailclient.models import UserEmail

def settings(request):
    users = CustomUser.objects.all()  # Use your CustomUser model
    signatures = EmailSignature.objects.all()
    templates = EmailTemplate.objects.all()

    context = {
        'users': users,
        'signatures': signatures,
        'templates': templates
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



from django.shortcuts import render, redirect
from .forms import EmailSignatureForm

def create_email_signature(request):
    if request.method == 'POST':
        form = EmailSignatureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('email_signature_list')  # Redirect to a page displaying the list of email signatures
    else:
        form = EmailSignatureForm()
    
    return render(request, 'create_email_signature.html', {'form': form})

from django.shortcuts import get_object_or_404, redirect
from .models import EmailSignature

def delete_signature(request, signature_id):
    signature = get_object_or_404(EmailSignature, id=signature_id)
    if request.method == 'POST':
        signature.delete()
    return redirect('email_signature_list')  # Assuming 'signature_list' is the name of your signature list view

def edit_email_signature(request, signature_id):
    signature = get_object_or_404(EmailSignature, id=signature_id)
    if request.method == 'POST':
        form = EmailSignatureForm(request.POST, instance=signature)
        if form.is_valid():
            form.save()
            return redirect('email_signature_list')  # Redirect to the list of email signatures
    else:
        form = EmailSignatureForm(instance=signature)
    
    return render(request, 'create_email_signature.html', {'form': form, 'is_edit': True})



from django.shortcuts import render
from .models import EmailSignature

def email_signature_list(request):
    signatures = EmailSignature.objects.all()
    return render(request, 'email_signature_list.html', {'signatures': signatures})


from django.shortcuts import render, redirect
from .models import EmailTemplate
from .forms import EmailTemplateForm

def list_email_templates(request):
    templates = EmailTemplate.objects.all()
    return render(request, 'email_template_list.html', {'templates': templates})

from attachments.views import add_attachment
from settings.models import TemplateAttachment


def create_email_template(request):
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            template = form.save()
            attachments = request.FILES.getlist('attachments')

            for attachment in attachments:
                template_attachment = TemplateAttachment(template=template, file=attachment)
                template_attachment.save()

            return redirect('list_email_templates')
    else:
        form = EmailTemplateForm()
    return render(request, 'create_email_template.html', {'form': form})

def edit_email_template(request, template_id):
    template = get_object_or_404(EmailTemplate, id=template_id)
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            return redirect('list_email_templates')
    else:
        form = EmailTemplateForm(instance=template)
    return render(request, 'create_email_template.html', {'form': form, 'is_edit': True})



from django.shortcuts import get_object_or_404, redirect

def delete_email_template(request, template_id):
    template = get_object_or_404(EmailTemplate, id=template_id)
    template.delete()
    return redirect('list_email_templates')



from django.shortcuts import render

def user_list(request):
    users = User.objects.all()  # Retrieve the list of users from your database
    return render(request, 'users.html', {'users': users})


from django.shortcuts import render
from emailclient.models import UserEmail

def email_accounts(request):
    emails = UserEmail.objects.all()  # Retrieve the list of emails from your database
    return render(request, 'email_accounts.html', {'emails': emails})


from django.shortcuts import render, redirect
from .forms import UserProfilePictureForm
from django.contrib.auth.decorators import login_required

@login_required
def my_profile(request):
    if request.method == 'POST':
        form = UserProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my_profile')  # Redirect back to the profile page after saving
    else:
        form = UserProfilePictureForm(instance=request.user)
    
    return render(request, 'my_profile.html', {'form': form})



