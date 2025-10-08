import json
import re
import string
from typing import Dict, List, Tuple, Union
from datetime import datetime


# -------------------- Utility Functions --------------------

def load_json_bank(filepath: str) -> Dict[str, List[str]]:
    """
    Safely load the question bank JSON file.
    Returns a dictionary: {level: {question_id: [keywords]}}
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            bank = {}
            if "questions" in data:
                for level, questions in data["questions"].items():
                    level_dict = {}
                    for q in questions:
                        qid = q.get("id", f"{level}_Q")
                        # Extract important words from the answer and keyword field
                        combined_kw = set()
                        combined_kw.update(tokenize(q.get("keyword", "")))
                        combined_kw.update(tokenize(q.get("answer", "")))
                        for opt in q.get("options", []):
                            combined_kw.update(tokenize(opt))
                        level_dict[qid] = list(combined_kw)
                    bank[level] = level_dict
            return bank
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[Error] Could not load JSON: {e}")
        return {}


def tokenize(text: str) -> List[str]:
    """Convert text to lowercase tokens without stopwords or punctuation."""
    if not text:
        return []
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    tokens = re.split(r'\W+', text)
    stopwords = {
        "a", "an", "the", "is", "and", "or", "of", "in", "to", "for", "on",
        "with", "as", "by", "at", "it", "that", "this", "are", "was", "be",
        "from", "if", "you", "your", "can", "will", "what", "how", "why",
        "i", "we", "they", "he", "she"
    }
    return [t for t in tokens if t and t not in stopwords]


def keyword_match_score(user_ans: str, correct_keywords: List[str]) -> float:
    """Find how many correct keywords appear in the user answer."""
    if not correct_keywords or not user_ans:
        return 0.0
    user_tokens = set(tokenize(user_ans))
    correct_tokens = set(tokenize(" ".join(correct_keywords)))
    if not correct_tokens:
        return 0.0
    matched = sum(1 for t in correct_tokens if t in user_tokens)
    return matched / len(correct_tokens)


def flag_for_score(score: float,
                   threshold_same: float = 0.5,
                   threshold_higher: float = 0.8) -> str:
    """Convert numeric score into a difficulty flag."""
    if score < threshold_same:
        return "Easier"
    elif score >= threshold_higher:
        return "Harder"
    else:
        return "Same"


def evaluate_user_level(user_answers: Dict[str, str],
                        level_bank: Dict[str, List[str]],
                        threshold_same: float = 0.5,
                        threshold_higher: float = 0.8) -> Tuple[Dict, float, str]:
    """Evaluate all answers for one level (e.g., beginner)."""
    per_question = {}
    total_score = 0.0
    count = 0

    for qid, keywords in level_bank.items():
        ans = user_answers.get(qid, "")
        score = keyword_match_score(ans, keywords)
        flag = flag_for_score(score, threshold_same, threshold_higher)
        per_question[qid] = {"score": round(score, 2), "flag": flag}
        total_score += score
        count += 1

    avg = total_score / count if count else 0.0
    overall_flag = flag_for_score(avg, threshold_same, threshold_higher)
    return per_question, round(avg, 2), overall_flag


LEVEL_ORDER = ["beginner", "intermediate", "hard"]

def next_level_from_flag(current_level: str, flag: str) -> str:
    """Find the next difficulty level based on flag."""
    try:
        idx = LEVEL_ORDER.index(current_level)
    except ValueError:
        idx = 0
    if flag == "Easier":
        return LEVEL_ORDER[max(0, idx - 1)]
    elif flag == "Harder":
        return LEVEL_ORDER[min(len(LEVEL_ORDER) - 1, idx + 1)]
    else:
        return current_level


def build_flag_record(user_id: str, field: str, current_level: str,
                      per_question: dict, avg_score: float, overall_flag: str) -> dict:
    """Build a record to save in MongoDB."""
    return {
        "user_id": user_id,
        "field": field,
        "level": current_level,
        "per_question": per_question,
        "avg_score": avg_score,
        "overall_flag": overall_flag,
        "timestamp": datetime.utcnow().isoformat()
    }
