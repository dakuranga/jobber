from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('settings/', views.settings, name='settings'),
    path('create_user/', views.create_user, name='create_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),


    


]
