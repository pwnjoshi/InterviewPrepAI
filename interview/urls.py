# interview/urls.py

from django.urls import path
from . import views

urlpatterns = [
  
    path('upload/', views.upload_resume, name='upload_resume'),
    path('dashboard/', views.dashboard, name='interview_dashboard'),
    path('start/', views.start_interview_view, name='start_interview'),
    path('question/', views.interview_question_view, name='interview_question'),

    # Results page with string session_id
    path('results/<str:session_id>/', views.results_view, name='interview_results'),
]