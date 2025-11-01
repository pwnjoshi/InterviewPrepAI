from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('dashboard/', views.dashboard, name='interview_dashboard'),
    
    path('interview/questions/', views.show_questions, name='show_questions'),
    path('interview/feedback/', views.show_feedback, name='show_feedback'),
]
