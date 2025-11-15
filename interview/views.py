from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Resume, Question, InterviewSession, Profile
from .resume_parser import extract_text_from_resume, extract_skills
from .db_operations import insert_resume, get_questions_by_skills, save_answers, get_session_data
from .utils import get_adaptive_questions, calculate_interview_score, score_single_answer
from .utils import get_fixed_interview_questions
from .answer_evaluation import keyword_match_score
import random

# NOTE: Views updated to use new models and utilities
# Includes integration with answerflagging.py and mongo_conn.py

@login_required(login_url='/login/')
def upload_resume(request):
    try:
        profile = Profile.objects.get(user=request.user)
        profile_exists = True
    except Profile.DoesNotExist:
        profile = None
        profile_exists = False

    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        if not resume_file:
            return render(request, 'interview/upload_resume.html', {'error': 'No file selected.'})

        # Parse the resume
        try:
            import os
            from django.conf import settings
            
            # Save file temporarily
            temp_path = os.path.join(settings.MEDIA_ROOT, 'resumes', resume_file.name)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            
            with open(temp_path, 'wb+') as destination:
                for chunk in resume_file.chunks():
                    destination.write(chunk)
            
            # Extract text from resume
            extracted_text = extract_text_from_resume(temp_path)
            
            # Extract skills
            extracted_skills = extract_skills(extracted_text)
            
            # Prepare resume data
            resume_data = {
                'username': request.user.username,
                'email': request.user.email or '',
                'phone': '',  # TODO: Extract from resume
                'skills': extracted_skills,
                'experience': extracted_text[:1000],  # First 1000 chars
                'education': '',  # TODO: Extract from resume
            }
            
            # Insert resume using mongo_conn utility
            result = insert_resume(resume_data)
            
            # Show success message to user
            if result.get('message'):
                messages.success(request, result['message'])
            else:
                messages.success(request, f"Resume uploaded successfully! Extracted {len(extracted_skills)} skills.")
            
            return redirect('interview_dashboard')
            
        except Exception as e:
            print(f"Could not parse resume or skills: {e}")
            import traceback
            traceback.print_exc()
            return render(request, 'interview/upload_resume.html', {'error': f'Error processing resume: {str(e)}'})

    return render(request, 'interview/upload_resume.html')


# dashboard view
@login_required(login_url='/login/')
def dashboard(request):
    try:
        # Get the user's profile
        profile = Profile.objects.get(user=request.user)
        
        # Get the latest resume
        latest_resume = Resume.objects.filter(username=request.user.username).order_by('-uploaded_at').first()
        
        context = {
            'profile': profile,
            'resume': latest_resume,
            'skills': latest_resume.skills if latest_resume else []
        }
        return render(request, 'interview/dashboard.html', context)
    except Profile.DoesNotExist:
        # If they don't have a profile, send them to the upload page
        return redirect('upload_resume')
    
# start interview view
@login_required(login_url='/login/')
def start_interview_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
        latest_resume = Resume.objects.filter(username=request.user.username).order_by('-uploaded_at').first()
    except Profile.DoesNotExist:
        return redirect('upload_resume')

    if not latest_resume:
        return redirect('upload_resume')

    # --- 1. Get Candidate's Skills ---
    skills = latest_resume.skills if latest_resume.skills else []
    
    # Ensure skills is a list
    if not isinstance(skills, list):
        skills = []

    # --- 2. Get user's current level from profile ---
    current_level = profile.current_level if hasattr(profile, 'current_level') else 'beginner'
    
    # --- 3. Get adaptive questions based on skills AND level ---
    questions = get_fixed_interview_questions(skills)


    # If no questions found, try without level filtering
    if not questions:
        all_questions = Question.objects.all()[:10]
        questions = [
            {
                "keywords": q.keywords if q.keywords else [],
                "question_text": q.question_text,
                "level": q.level,
                "answer": q.answer,
            }
            for q in all_questions
        ]
    
    if not questions:
        # No questions in database at all
        return render(request, 'interview/dashboard.html', {
            'error': 'No questions available. Please contact administrator.'
        })

    # --- 4. Store in session (including current level) ---
    request.session['interview_questions'] = questions
    request.session['current_question_index'] = 0
    request.session['user_answers'] = {}
    request.session['interview_level'] = current_level

    # --- 5. Redirect to the first question page ---
    return redirect('interview_question')

@login_required(login_url='/login/')
def interview_question_view(request):
    # Get interview data from the user's session
    questions = request.session.get('interview_questions', [])
    current_index = request.session.get('current_question_index', 0)
    user_answers = request.session.get('user_answers', {})
    interview_level = request.session.get('interview_level', 'beginner')

    # If any data is missing, the interview hasn't started
    if not questions or current_index >= len(questions):
        return redirect('interview_dashboard')

    # --- Handle Answer Submission ---
    if request.method == 'POST':
        answer_text = request.POST.get('answer', '')
        question = questions[current_index]

        # Save the answer in session
        user_answers[question['question_text']] = answer_text
        request.session['user_answers'] = user_answers

        # Move to the next question
        next_index = current_index + 1
        request.session['current_question_index'] = next_index

        # Check if the interview is over
        if next_index >= len(questions):
            # End interview - save to database
            latest_resume = Resume.objects.filter(username=request.user.username).order_by('-uploaded_at').first()
            profile = Profile.objects.get(user=request.user)
            
            # Calculate scores using answerflagging
            total_score = 0
            scored_answers = {}
            
            for q_text, ans_text in user_answers.items():
                # Find the question to get keywords
                question_data = next((q for q in questions if q['question_text'] == q_text), None)
                if question_data:
                    keywords = question_data.get('keywords', [])
                    # Score the answer
                    score = keyword_match_score(ans_text, keywords)
                    total_score += score
                    scored_answers[q_text] = {
                        'answer': ans_text,
                        'score': round(score, 2),
                        'keywords': keywords
                    }
            
            avg_score = total_score / len(questions) if questions else 0
            
            # Use evaluate_interview_answers for full evaluation (import at top if needed)
            from .utils import evaluate_interview_answers
            
            # Prepare user_answers_for_eval mapping question_id to answer text
            user_answers_for_eval = {q_text: ans_text for q_text, ans_text in user_answers.items()}
            
            # Get evaluation results
            eval_results = None
            try:
                eval_results = evaluate_interview_answers(
                    user_id=profile.unique_user_id,
                    field='general',  # You can extract from skills
                    current_level=interview_level,
                    user_answers=user_answers_for_eval
                )
            except Exception as e:
                print(f"Evaluation error: {e}")
            
            # Save answers using db_operations utility with enhanced data
            from .models import InterviewSession as InterviewSessionModel
            from django.utils.crypto import get_random_string
            
            session_id = get_random_string(12)
            
            # Create interview session with level tracking
            interview_session = InterviewSessionModel(
                session_id=session_id,
                username=request.user.username,
                skills=latest_resume.skills if latest_resume else [],
                answers=scored_answers,
                score=round(avg_score, 2),
                current_level=interview_level,
                recommended_next_level=eval_results['recommended_next_level'] if eval_results else interview_level,
                evaluation_flag=eval_results['overall_flag'] if eval_results else 'Same',
                flag_records=eval_results['flag_record'] if eval_results else {}
            )
            interview_session.save()
            
            # Update user's level if they should progress
            if eval_results and eval_results['recommended_next_level'] != interview_level:
                profile.current_level = eval_results['recommended_next_level']
                profile.save()
            
            # Show completion message
            messages.success(request, f"Interview completed! Your score: {round(avg_score * 100, 1)}%")
            
            # Clear session
            del request.session['interview_questions']
            del request.session['current_question_index']
            del request.session['user_answers']
            if 'interview_level' in request.session:
                del request.session['interview_level']
            
            return redirect('interview_results', session_id=session_id)
        else:
            # Go to the next question
            return redirect('interview_question')

    # --- Show the Current Question (GET Request) ---
    current_question = questions[current_index]

    context = {
        'question': {'text': current_question.get('question_text', '')},
        'question_number': current_index + 1,
        'total_questions': len(questions),
        'current_level': interview_level
    }
    return render(request, 'interview/question_page.html', context)



@login_required(login_url='/login/')
def results_view(request, session_id):
    # Get session data using mongo_conn utility
    session_data = get_session_data(session_id)
    
    if not session_data:
        return redirect('interview_dashboard')
    
    # Verify it's the current user's session
    if session_data['username'] != request.user.username:
        return redirect('interview_dashboard')
    
    # Get the InterviewSession object for level information
    try:
        from .models import InterviewSession
        interview_session = InterviewSession.objects.get(session_id=session_id)
    except InterviewSession.DoesNotExist:
        interview_session = None
    
    # Calculate detailed scores
    score_details = calculate_interview_score(session_id)

    context = {
        'session': {
            'final_score': session_data['score'],
            'username': session_data['username'],
            'current_level': interview_session.current_level if interview_session else 'beginner',
            'recommended_next_level': interview_session.recommended_next_level if interview_session else None,
            'evaluation_flag': interview_session.evaluation_flag if interview_session else None,
        },
        'answers': session_data['answers'],
        'skills': session_data['skills'],
        'score_details': score_details
    }
    
    return render(request, 'interview/results_page.html', context)
