from django.contrib import admin
from .models import CandidateProfile, Question, InterviewSession, Answer

# This tells the admin site to show these models
admin.site.register(CandidateProfile)
admin.site.register(Question)
admin.site.register(InterviewSession)
admin.site.register(Answer)