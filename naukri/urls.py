from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import linkedin_view
from django.urls import re_path
from . import views

urlpatterns = [
    path('linkedin-view/', linkedin_view, name='linkedin_view'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)