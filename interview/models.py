from djongo import models
from django.contrib.auth.models import User



#  Resume Storage Model
class Resume(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    skills = models.JSONField()  # list of extracted skills
    experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}'s Resume"


#  Question Storage Model
class Question(models.Model):
    keywords = models.JSONField()  # list of keywords
    level = models.CharField(max_length=50, default="beginner")
    question_text = models.TextField()
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.level.capitalize()} - {', '.join(self.keywords)}"


#  Interview (Session) Model
class InterviewSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    skills = models.JSONField()
    answers = models.JSONField()
    score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session: {self.session_id}"


#  Profile Model (Authenticated User)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=100, unique=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.name} ({self.user.username})"

