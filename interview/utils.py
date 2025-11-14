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


# ============================================================
# FIXED QUESTION SELECTION FOR INTERVIEW (10 QUESTIONS TOTAL)
# ============================================================

def get_fixed_interview_questions(skills):
    """
    Return EXACTLY 10 questions for an interview:
       - 4 beginner
       - 3 intermediate
       - 3 hard

    Args:
        skills (list): Extracted skills from resume

    Returns:
        list of question dictionaries
    """

    # If skills are invalid or empty, default to empty list
    if not skills or not isinstance(skills, list):
        skills = []

    # Fetch questions by skills (large pool)
    all_questions = get_questions_by_skills(skills, limit=200)

    # If no skill-based questions found, use all questions
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

    # Split by difficulty
    beginner = [q for q in all_questions if q.get("level") == "beginner"]
    intermediate = [q for q in all_questions if q.get("level") == "intermediate"]
    hard = [q for q in all_questions if q.get("level") == "hard"]

    # Helper to pick N questions
    def pick(question_list, n):
        if len(question_list) >= n:
            return question_list[:n]
        return question_list

    selected = []

    # Pick fixed difficulty counts
    selected.extend(pick(beginner, 4))
    selected.extend(pick(intermediate, 3))
    selected.extend(pick(hard, 3))

    # If less than 10, fill from remaining pool
    if len(selected) < 10:
        remaining = [q for q in all_questions if q not in selected]
        selected.extend(remaining[:(10 - len(selected))])

    return selected[:10]


# ============================================================
# ANSWER SCORING FOR EACH QUESTION
# ============================================================

def score_single_answer(answer_text, expected_keywords):
    """
    Score a single answer based on keyword matching.

    Args:
        answer_text: User's answer text
        expected_keywords: List of expected keywords

    Returns:
        float: score between 0 and 1
    """
    return keyword_match_score(answer_text, expected_keywords)


# ============================================================
# ADAPTIVE SYSTEM (OLD) - NOW USED ONLY FOR EVALUATION
# ============================================================

def evaluate_interview_answers(user_id, field, current_level, user_answers):
    """
    Evaluate user's answers and determine next difficulty level.

    Args:
        user_id: User identifier
        field: Question category
        current_level: beginner/intermediate/hard
        user_answers: Dict -> question_id : answer_text

    Returns:
        dict: evaluation and scoring summary
    """

    # Fetch expected questions for this level
    questions = Question.objects.filter(level=current_level)

    # Build mapping: question_id -> expected_keywords
    level_bank = {str(q.id): q.keywords for q in questions}

    # Perform scoring
    per_question, avg_score, overall_flag = evaluate_user_level(
        user_answers, 
        level_bank
    )

    # Determine next difficulty
    next_level = next_level_from_flag(current_level, overall_flag)

    # Prepare DB-ready flag record
    flag_record = build_flag_record(
        user_id, 
        field, 
        current_level,
        per_question, 
        avg_score, 
        overall_flag
    )

    return {
        "per_question_scores": per_question,
        "average_score": avg_score,
        "overall_flag": overall_flag,
        "current_level": current_level,
        "recommended_next_level": next_level,
        "flag_record": flag_record
    }


# ============================================================
# OLD ADAPTIVE QUESTION FUNCTION (KEPT FOR COMPATIBILITY)
# ============================================================

def get_adaptive_questions(skills, current_level='beginner', limit=5):
    """
    Adaptive fallback (unused in fixed interviews).
    
    Returns questions matching a difficulty level.
    """

    if not skills or not isinstance(skills, list):
        skills = []

    all_questions = get_questions_by_skills(skills, limit=100) if skills else []

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

    level_questions = [
        q for q in all_questions 
        if q.get('level', 'beginner') == current_level
    ]

    return level_questions[:limit]


# ============================================================
# FINAL SCORING FOR WHOLE INTERVIEW SESSION
# ============================================================

def calculate_interview_score(session_id):
    """
    Generate the final score + grade for an interview session.

    Args:
        session_id: Interview Session ID

    Returns:
        dict: score, percentage, feedback
    """

    session_data = get_session_data(session_id)

    if not session_data:
        return None

    answers = session_data.get("answers", {})
    total_questions = len(answers)

    if total_questions == 0:
        return {
            "total_score": 0,
            "percentage": 0,
            "grade": "N/A",
            "feedback": "No answers submitted"
        }

    score = session_data.get("score", 0)
    percentage = score * 100 if score <= 1 else score

    # Grade assignment
    if percentage >= 90:
        grade = "A+"
        feedback = "Excellent! Outstanding performance."
    elif percentage >= 80:
        grade = "A"
        feedback = "Great job! Very good understanding."
    elif percentage >= 70:
        grade = "B"
        feedback = "Good work! Solid understanding."
    elif percentage >= 60:
        grade = "C"
        feedback = "Fair performance. Room for improvement."
    elif percentage >= 50:
        grade = "D"
        feedback = "Needs improvement. Consider reviewing the topics."
    else:
        grade = "F"
        feedback = "Needs significant improvement. Please study more."

    return {
        "session_id": session_id,
        "username": session_data.get("username"),
        "total_questions": total_questions,
        "total_score": score,
        "percentage": round(percentage, 2),
        "grade": grade,
        "feedback": feedback,
        "skills_tested": session_data.get("skills", [])
    }
