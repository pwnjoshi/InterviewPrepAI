from pymongo import MongoClient
def get_database():
    client = MongoClient("mongodb://localhost:27017/")  # local MongoDB
    db = client.nexora_db
    return db
def insert_resume(resume_data):
    db = get_database()
    resume_col = db.resume
    resume_col.insert_one(resume_data)
    print("✅ Resume inserted successfully")


def get_questions_by_skills(skills, limit=10):
    db = get_database()
    question_col = db.question
    # Fetch questions matching any skill
    questions = question_col.find({"skill": {"$in": skills}}, {"_id":0}).limit(limit)
    return list(questions)


def save_answers(answers_data):
    db = get_database()
    interview_col = db.interview
    interview_col.insert_one(answers_data)
    print("✅ Answers saved successfully")


def get_session_data(session_id):
  def get_session_data(session_id):
    db = get_database()
    interview_col = db.interview
    session = interview_col.find_one({"session_id": session_id}, {"_id":0})
    return session

