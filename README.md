## Nexora - InterviewPrepAI

Your personal, lightweight interview prep assistant. Upload a resume, practice tailored questions, and get simple feedback—all in a clean Django app.

---

## What’s inside

- Resume upload (PDF/DOCX)
- Skill-based question flow
- Simple feedback after submission
- SQLite by default; MongoDB optional (code present, not required)

---

## Project structure

```
.
├─ db.sqlite3
├─ integrate_flags.py
├─ manage.py
├─ README.md
├─ requirements.txt
├─ authentication/
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  └─ migrations/
├─ interview/
│  ├─ admin.py
│  ├─ answers_flagging.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ mongo_conn.py              
│  ├─ resume_parser.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  ├─ static/
│  │  └─ css/styles.css
│  └─ templates/
│     ├─ feedback.html
│     ├─ index.html
│     ├─ login.html
│     ├─ questions.html
│     └─ interview/
│        ├─ dashboard.html
│        └─ upload_resume.html
├─ media/
│  └─ resumes/
└─ nexora_project/
   ├─ asgi.py
   ├─ settings.py
   ├─ urls.py
   └─ wsgi.py
```

---

## Quick start (Windows PowerShell)

1) Clone and enter the project folder

```powershell
git clone https://github.com/pwnjoshi/InterviewPrepAI.git
cd InterviewPrepAI
```

2) Create and activate a virtual environment

```powershell
python -m venv venv
./venv/Scripts/Activate.ps1
```

3) Install dependencies and run migrations

```powershell
pip install -r requirements.txt
python manage.py migrate
```

4) Run the server

```powershell
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your browser.

---

## How to use

1) Upload your resume on the home/dashboard page
2) Answer the presented questions
3) Submit to see basic feedback on your responses

---

## Tech

- Python 3.8+
- Django 5.x
- SQLite (default) change it 
- PyMuPDF/python-docx for resume parsing
- MongoDB 
---

Contributions and issues are welcome. Keep changes small and focused.
