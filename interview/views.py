from django.shortcuts import render, redirect

def upload_resume(request):
    """Handle resume upload"""
    if request.method == 'POST':
        # TODO: Implement file upload handling
        # TODO: Integrate MongoDB for resume storage
        # TODO: Parse resume to extract skills
        
        # Demo: Set session data
        request.session['resume_uploaded'] = True
        request.session['candidate_name'] = 'Demo User'
        return redirect('show_questions')
    
    return render(request, 'upload.html')

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
    # TODO: Integrate AI for feedback generation
    # TODO: Calculate and display scores
    
    # Demo data
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
