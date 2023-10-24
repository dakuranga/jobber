from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_management.urls')),
    path('', include('clients.urls')),
    path('', include('jobs.urls')),
    path('', include('candidates.urls')),
    path('', include('dashboard.urls')),
    path('', include('reports.urls')),
    path('', include('interviews.urls')),
    path('', include('emailclient.urls')),
    path('', include('naukri.urls')),
    path('', include('settings.urls')),
    path('', include('jobportal.urls')),
]
