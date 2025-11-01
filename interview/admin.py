from django.contrib import admin
from .models import CandidateProfile, Question, InterviewSession, Answer

admin.site.site_title = "Nexora Admin Portal"
admin.site.site_header = "Nexora Admin Portal"
admin.site.index_title = "Welcome to Nexora Admin Portal"

# This tells the admin site to show these models
admin.site.register(CandidateProfile)
admin.site.register(Question)
admin.site.register(InterviewSession)
admin.site.register(Answer)