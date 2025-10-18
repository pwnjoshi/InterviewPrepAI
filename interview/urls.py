# interview/urls.py

from django.urls import path
from . import views

urlpatterns = [
  
    path('upload/', views.upload_resume, name='upload_resume'),
    path('dashboard/', views.dashboard, name='interview_dashboard'),
]