# interview/utils.py
# Utility functions for interview management

from .answer_evaluation import (
    evaluate_user_level,
    build_flag_record,
    next_level_from_flag,
    keyword_match_score
)
from .db_operations import get_questions_by_skills, save_answers, get_session_data
from .models import Question


def evaluate_interview_answers(user_id, field, current_level, user_answers):
    """
    Evaluate user's interview answers and determine next difficulty level.
    
    Args:
        user_id: Unique identifier for the user
        field: Field of questions (e.g., 'python', 'javascript')
        current_level: Current difficulty level ('beginner', 'intermediate', 'hard')
        user_answers: Dict mapping question IDs to user's answer text
    
    Returns:
        dict: Evaluation results with scores, flags, and recommendations
    """
    # Get questions from database for this level
    questions = Question.objects.filter(level=current_level)
    
    # Build level bank (question_id -> keywords)
    level_bank = {}
    for q in questions:
        level_bank[str(q.id)] = q.keywords
    
    # Evaluate answers
    per_question, avg_score, overall_flag = evaluate_user_level(
        user_answers, 
        level_bank
    )
    
    # Determine next level
    next_level = next_level_from_flag(current_level, overall_flag)
    
    # Build flag record for storage
    flag_record = build_flag_record(
        user_id, 
        field, 
        current_level,
        per_question, 
        avg_score, 
        overall_flag
    )
    
    return {
        'per_question_scores': per_question,
        'average_score': avg_score,
        'overall_flag': overall_flag,
        'current_level': current_level,
        'recommended_next_level': next_level,
        'flag_record': flag_record
    }


def score_single_answer(answer_text, expected_keywords):
    """
    Score a single answer based on keyword matching.
    
    Args:
        answer_text: User's answer as string
        expected_keywords: List of expected keywords
    
    Returns:
        float: Score between 0 and 1
    """
    return keyword_match_score(answer_text, expected_keywords)


def get_adaptive_questions(skills, current_level='beginner', limit=5):
    """
    Get adaptive questions based on user skills and current level.
    
    Args:
        skills: List of user's skills
        current_level: Current difficulty level
        limit: Maximum number of questions to return
    
    Returns:
        list: List of question dictionaries
    """
    # Ensure skills is a list
    if not skills or not isinstance(skills, list):
        skills = []
    
    # Get questions matching skills
    all_questions = get_questions_by_skills(skills, limit=100) if skills else []
    
    # If no skill-matched questions, get all questions
    if not all_questions:
        all_questions = [
            {
                "keywords": q.keywords if q.keywords else [],
                "question_text": q.question_text,
                "level": q.level,
                "answer": q.answer,
            }
            for q in Question.objects.all()
        ]
    
    # Filter by level
    level_questions = [
        q for q in all_questions 
        if q.get('level', 'beginner') == current_level
    ]
    
    # If not enough questions at this level, include some from adjacent levels
    if len(level_questions) < limit:
        level_order = ['beginner', 'intermediate', 'hard']
        try:
            current_idx = level_order.index(current_level)
            # Add questions from adjacent levels
            for offset in [1, -1]:
                adj_idx = current_idx + offset
                if 0 <= adj_idx < len(level_order):
                    adj_level = level_order[adj_idx]
                    adj_questions = [
                        q for q in all_questions 
                        if q.get('level', 'beginner') == adj_level
                    ]
                    level_questions.extend(adj_questions)
                    if len(level_questions) >= limit:
                        break
        except ValueError:
            pass
    
    return level_questions[:limit]


def calculate_interview_score(session_id):
    """
    Calculate detailed score for an interview session.
    
    Args:
        session_id: Interview session ID
    
    Returns:
        dict: Detailed scoring information
    """
    session_data = get_session_data(session_id)
    
    if not session_data:
        return None
    
    answers = session_data.get('answers', {})
    total_questions = len(answers)
    
    if total_questions == 0:
        return {
            'total_score': 0,
            'percentage': 0,
            'grade': 'N/A',
            'feedback': 'No answers submitted'
        }
    
    # Calculate percentage
    score = session_data.get('score', 0)
    percentage = (score * 100) if score <= 1 else score
    
    # Determine grade
    if percentage >= 90:
        grade = 'A+'
        feedback = 'Excellent! Outstanding performance.'
    elif percentage >= 80:
        grade = 'A'
        feedback = 'Great job! Very good understanding.'
    elif percentage >= 70:
        grade = 'B'
        feedback = 'Good work! Solid understanding.'
    elif percentage >= 60:
        grade = 'C'
        feedback = 'Fair performance. Room for improvement.'
    elif percentage >= 50:
        grade = 'D'
        feedback = 'Needs improvement. Consider reviewing the topics.'
    else:
        grade = 'F'
        feedback = 'Needs significant improvement. Please study more.'
    
    return {
        'session_id': session_id,
        'username': session_data.get('username'),
        'total_questions': total_questions,
        'total_score': score,
        'percentage': round(percentage, 2),
        'grade': grade,
        'feedback': feedback,
        'skills_tested': session_data.get('skills', [])
    }
