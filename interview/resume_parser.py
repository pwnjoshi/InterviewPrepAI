import docx
import fitz
import re
import os

class ResumeParser:
    def __init__(self):
        self.keywords = {
            "Core CS": ["Python", "Java", "C++", "C", "JavaScript", "SQL", "Data Structures", "Algorithms", "OOP", "Object-Oriented Programming", "Big O Notation", "Operating Systems", "Computer Networks"],
            "Web Dev": ["HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask", "Spring Boot", "REST API", "GraphQL"],
            "AI/ML/DS": ["TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Classification", "Regression", "Clustering", "Deep Learning", "Neural Networks", "NLP", "Natural Language Processing", "Data Visualization", "Feature Engineering", "Model Training", "GAN", "ARIMA", "Sentiment Analysis", "Computer Vision"],
            "Cyber Security": ["Cryptography", "Network Security", "Penetration Testing", "Ethical Hacking", "Malware Analysis", "Firewalls", "SQL Injection", "XSS", "Cross-Site Scripting", "Vulnerability Assessment"],
            "DB/Cloud/DevOps": ["MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle SQL", "AWS", "Amazon Web Services", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes", "Git", "CI/CD"]
        }

    def _extract_text_from_docx(self, filepath):
        try:
            doc = docx.Document(filepath)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            return ""

    def _extract_text_from_pdf(self, filepath):
        try:
            with fitz.open(filepath) as doc:
                return "".join(page.get_text() for page in doc)
        except Exception as e:
            return ""

    def parse(self, filepath):
        if not os.path.exists(filepath):
            return set()

        text = ""
        if filepath.lower().endswith(".docx"):
            text = self._extract_text_from_docx(filepath)
        elif filepath.lower().endswith(".pdf"):
            text = self._extract_text_from_pdf(filepath)
        else:
            return set()
            
        if not text:
            return set()

        resume_text_lower = text.lower()
        found_keywords = set()

        for category, terms in self.keywords.items():
            for term in terms:
                if re.search(r'\b' + re.escape(term.lower()) + r'\b', resume_text_lower):
                    found_keywords.add(term)
            
        return found_keywords

