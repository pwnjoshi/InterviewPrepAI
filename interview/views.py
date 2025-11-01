from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import os

def upload_resume(request):
    """Handle resume upload""" 
    """but jab tum models banaoge ye logic change kr lena to store in mongodb direcly ( just a save functino hoga yaha) """
    if request.method == 'POST':

        if 'resume' in request.FILES:
            resume_file = request.FILES['resume']
            
            allowed_extensions = ['.pdf', '.docx']
            file_extension = os.path.splitext(resume_file.name)[1].lower()
            
            if file_extension not in allowed_extensions:
                return render(request, 'interview/upload_resume.html', {
                    'error': 'Please upload only PDF or DOCX files.'
                })
            
            fs = FileSystemStorage(location='media/resumes')
            filename = fs.save(resume_file.name, resume_file)
            file_url = fs.url(filename)

            request.session['resume_uploaded'] = True
            request.session['resume_filename'] = filename
            request.session['resume_path'] = os.path.join('media', 'resumes', filename)
            request.session['candidate_name'] = 'Demo User'  # You can parse this from resume later
            
            # TODO: Parse resume to extract skills
            # TODO: Integrate MongoDB for resume storage
            
            return redirect('interview_dashboard')
        else:
            return render(request, 'interview/upload_resume.html', {
                'error': 'Please select a file to upload.'
            })
    
    return render(request, 'interview/upload_resume.html')

@login_required(login_url='/login/')
def dashboard(request):
        # Get the user's profile
        # If they don't have a profile, send them to the upload page
        return render(request, 'interview/dashboard.html')

def show_questions(request):
    """Display interview questions"""
    if not request.session.get('resume_uploaded'):
        return redirect('upload_resume')
        
    if request.method == 'POST':
        # TODO: Store answers in MongoDB
        
        # Demo: Store answers in session
        answers = {}
        for key, value in request.POST.items():
            if key.startswith('answer_'):
                answers[key] = value
        request.session['answers'] = answers
        return redirect('show_feedback')
    
    # TODO: Load questions from MongoDB based on candidate skills
    
    # Demo data
    context = {
        'candidate_name': 'Demo User',
        'questions': [
            {'id': 1, 'text': 'Tell me about your experience with Python.'},
            {'id': 2, 'text': 'Describe a challenging project you worked on.'},
            {'id': 3, 'text': 'What are your career goals?'}
        ]
    }
    return render(request, 'questions.html', context)

def show_feedback(request):
    """Display feedback on answers"""
    if not request.session.get('answers'):
        return redirect('upload_resume')
        
    # TODO: Fetch answers from MongoDB
    # TODO: feedback generation
    # TODO: Calculate and display scores
    
    # Demo data , QUESSTIONS mongodb se feth honge 
    answers = request.session.get('answers', {})
    context = {
        'candidate_name': 'Demo User',
        'total_questions': 3,
        'answered_questions': len(answers),
        'feedback_items': [
            {
                'question': 'Tell me about your experience with Python.',
                'answer': answers.get('answer_1', 'No answer provided'),
                'score': 85,
                'feedback': 'Good technical knowledge demonstrated.'
            },
            {
                'question': 'Describe a challenging project you worked on.',
                'answer': answers.get('answer_2', 'No answer provided'),
                'score': 78,
                'feedback': 'Provide more specific details about challenges faced.'
            },
            {
                'question': 'What are your career goals?',
                'answer': answers.get('answer_3', 'No answer provided'),
                'score': 92,
                'feedback': 'Clear vision and well-articulated goals.'
            }
        ]
    }
    
    # Clear session for next interview
    request.session.flush()
    
    return render(request, 'feedback.html', context)
