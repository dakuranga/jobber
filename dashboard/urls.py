from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('masterdashboard/', views.master_dashboard, name='master_dashboard'),
    path('master_dashboard/<str:date_filter>/', views.master_dashboard, name='master_dashboard_filter'),
    path('export_custom_report/', views.export_custom_report, name='export_custom_report'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
