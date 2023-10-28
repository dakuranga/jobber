from django.urls import path, re_path
from . import views
from settings.views import create_email_template, list_email_templates
from ckeditor_uploader import views as ckeditor_views
from django.views.decorators.cache import never_cache
from .views import my_profile



urlpatterns = [
    # Other URL patterns
    path('settings/', views.settings, name='settings'),
    path('create_user/', views.create_user, name='create_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),


    path('settings/create-email-signature/', views.create_email_signature, name='create_email_signature'),
    path('delete_signature/<int:signature_id>/', views.delete_signature, name='delete_signature'),
    path('edit_signature/<int:signature_id>/', views.edit_email_signature, name='edit_signature'),


    path('settings/email_signatures/', views.email_signature_list, name='email_signature_list'),
    re_path(r'^upload/', ckeditor_views.upload, name='ckeditor_upload'),
    re_path(r'^browse/', never_cache(ckeditor_views.browse), name='ckeditor_browse'),

    
    path('settings/create-template/', views.create_email_template, name='create_email_template'),
    path('settings/edit/<int:template_id>/', views.edit_email_template, name='edit_email_template'),
    path('settings/delete/<int:template_id>/', views.delete_email_template, name='delete_email_template'),
    path('settings/view-templates/', views.list_email_templates, name='list_email_templates'),


    path('settings/users/', views.user_list, name='user_list'),

    path('settings/emails/', views.email_accounts, name='email_accounts'),
    

    path('settings/profile/', my_profile, name='my_profile'),



    


]
