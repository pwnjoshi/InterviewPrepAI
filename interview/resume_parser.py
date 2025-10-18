# interview/resume_parser.py

import pdfplumber
import docx
import os

import spacy # IMPORT SPACY
from spacy.matcher import PhraseMatcher # IMPORT THE MATCHER


# Load the small English model
# We do this once here so it's ready when the server starts
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading 'en_core_web_sm' model. This might take a moment...")
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def extract_text_from_resume(file_path):
    _, extension = os.path.splitext(file_path)
    
    text = ""
    
    try:
        if extension == '.pdf':
            # Extract text from PDF
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        
        elif extension == '.docx':
            # Extract text from DOCX
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
            
        else:
            # Unsupported file type
            return f"Unsupported file type: {extension}"
            
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return f"Error reading file: {e}"



# ye hamara extract skill function hai - will be called from views.py
def extract_skills(text):

    SKILL_LIST = [
        "python", "django", "flask", "java", "c++", "c#", "ruby",
        "javascript", "react", "angular", "vue", "node.js",
        "html", "css", "bootstrap", "tailwind",
        "sql", "mysql", "postgresql", "mongodb", "firebase",
        "git", "github", "docker", "kubernetes", "aws", "azure", "gcp",
        "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
        "pandas", "numpy", "matplotlib",
        "data structures", "algorithms",
        "api", "rest api", "json", "xml"
    ]
    
    # Process the text with spaCy
    doc = nlp(text.lower()) # Convert text to lowercase for easier matching
    
    # Initialize the PhraseMatcher
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    # Create pattern documents from the skill list
    skill_patterns = [nlp.make_doc(skill) for skill in SKILL_LIST]
    
    # Add the patterns to the matcher
    matcher.add("SKILL_MATCHER", skill_patterns)
    
    # Find all matches in the document
    matches = matcher(doc)
    
    # Get the unique matched skills (as strings)
    found_skills = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        found_skills.add(span.text)
        
    # Return as a list
    return list(found_skills)