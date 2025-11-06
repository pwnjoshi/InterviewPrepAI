from .models import Resume, Question, InterviewSession, Profile
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string



#  Insert Resume + Show User ID

def insert_resume(resume_data):
    username = resume_data.get("username")
    email = resume_data.get("email")

    #  Check if user exists or create a new one
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email or ""}
    )

    #  Check if profile exists or create new one
    profile, profile_created = Profile.objects.get_or_create(
        user=user,
        defaults={
            "user_id": f"USER_{user.id}",
            "name": username,
            "email": email or ""
        }
    )

    # Create and save resume
    resume = Resume.objects.create(**resume_data)
    resume.save()

    print(f" Resume inserted successfully for {username}")
    print(f" User ID: {profile.user_id}")

    return {"resume": resume, "user_id": profile.user_id}



# Fetch Questions Based on Skills
def get_questions_by_skills(skills, limit=10):
    lower_skills = [s.lower() for s in skills]
    matched_questions = []

    for q in Question.objects.all():
        question_keywords = [k.lower() for k in q.keywords]
        if any(skill in k or k in skill for k in question_keywords for skill in lower_skills):
            matched_questions.append({
                "keywords": q.keywords,
                "question_text": q.question_text,
                "level": q.level,
                "answer": q.answer,
            })
            if len(matched_questions) >= limit:
                break

    return matched_questions



# Save Interview Answers
def save_answers(username, skills, answers, score):
    session_id = get_random_string(12)
    InterviewSession.objects.create(
        session_id=session_id,
        username=username,
        skills=skills,
        answers=answers,
        score=score
    )
    print(f" Answers saved successfully for {username}")
    return session_id


#  Retrieve Saved Session Data
def get_session_data(session_id):
    try:
        session = InterviewSession.objects.get(session_id=session_id)
        return {
            "username": session.username,
            "skills": session.skills,
            "answers": session.answers,
            "score": session.score,
        }
    except InterviewSession.DoesNotExist:
        return None
