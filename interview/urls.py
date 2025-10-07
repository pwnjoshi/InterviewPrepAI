from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_resume, name='upload_resume'),
    path('questions/', views.show_questions, name='show_questions'),
    path('feedback/', views.show_feedback, name='show_feedback'),
]
