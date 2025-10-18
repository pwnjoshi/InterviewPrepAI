# interview/models.py

from django.db import models
from django.conf import settings

class CandidateProfile(models.Model):
  user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='candidate_profile'
  )
  resume = models.FileField(upload_to='resumes/')
  
  #  parsed content from resume processing
  full_text = models.TextField(blank=True, null=True)
  parsed_skills = models.JSONField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"CandidateProfile(user={self.user.username})"