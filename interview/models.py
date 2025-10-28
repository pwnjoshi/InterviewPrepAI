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
  

# This model stores the questions in your question bank
class Question(models.Model):
    CATEGORY_CHOICES = (
        ('technical', 'Technical'),
        ('hr', 'HR'),
        ('behavioral', 'Behavioral'),
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    text = models.TextField()
    expected_keywords = models.JSONField(blank=True, null=True) # e.g., ["OOP", "Inheritance"]

    def __str__(self):
        return f"{self.get_category_display()} - {self.text[:50]}..."


# This model stores the results of one interview session
class InterviewSession(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    final_score = models.FloatField(blank=True, null=True)
    feedback_summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.candidate.user.username} on {self.date.date()}"


# This model stores each individual answer in that session
class Answer(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    score = models.FloatField(default=0) # Give it a default value
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Answer from {self.session.candidate.user.username}"