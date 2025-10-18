# Contributing to Nexora 🤝

First off, thank you for considering contributing to Nexora! It's people like you that make Nexora such a great tool for revolutionizing the hiring process.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Community](#community)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inspiring community for all.

### Our Standards

**Positive behaviors include:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behaviors include:**
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

---

## 🚀 How Can I Contribute?

### 1. Reporting Bugs 🐛

Before creating bug reports, please check the existing issues to avoid duplicates.

**When reporting a bug, include:**
- A clear and descriptive title
- Exact steps to reproduce the problem
- Expected behavior vs. actual behavior
- Screenshots (if applicable)
- Your environment:
  - OS (Windows/macOS/Linux)
  - Python version
  - Django version
  - MongoDB version

**Example Bug Report:**
```markdown
**Title**: Resume upload fails with PDF files larger than 5MB

**Description**: When uploading a PDF resume larger than 5MB, 
the system throws a 413 error.

**Steps to Reproduce**:
1. Go to /interview/upload/
2. Select a PDF file > 5MB
3. Click "Upload and Create Profile"
4. See error

**Expected**: File should upload successfully
**Actual**: 413 Request Entity Too Large error

**Environment**:
- OS: Windows 11
- Python: 3.10.11
- Django: 3.2.25
```

### 2. Suggesting Enhancements 💡

Enhancement suggestions are tracked as GitHub issues.

**When suggesting enhancements, include:**
- A clear and descriptive title
- Detailed description of the proposed feature
- Why this enhancement would be useful
- Possible implementation approach (optional)

### 3. Code Contributions 💻

#### Types of Contributions We Welcome:

- **🐛 Bug Fixes**: Fix existing issues
- **✨ New Features**: Add new functionality
- **📝 Documentation**: Improve README, docstrings, comments
- **🎨 UI/UX**: Enhance frontend design
- **⚡ Performance**: Optimize code and queries
- **🧪 Tests**: Add or improve test coverage
- **🔧 Refactoring**: Improve code structure

---

## 🛠️ Development Setup

### Prerequisites

- Python 3.10
- MongoDB (local or Atlas)
- Git

### Setup Steps

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/nexora.git
   cd nexora
   ```

2. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/nexora.git
   ```

3. **Create virtual environment**
   ```bash
   # Windows
   py -3.10 -m venv .venv310
   .\.venv310\Scripts\Activate

   # macOS/Linux
   python3.10 -m venv .venv310
   source .venv310/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

5. **Setup database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

---

## 📏 Coding Standards

### Python Style Guide (PEP 8)

- Use **4 spaces** for indentation (no tabs)
- Maximum line length: **79 characters** for code, **72 for comments**
- Use **snake_case** for functions and variables
- Use **PascalCase** for class names
- Use **UPPER_CASE** for constants

### Django Best Practices

```python
# ✅ Good
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def dashboard(request):
    """Display candidate dashboard with parsed skills."""
    profile = CandidateProfile.objects.get(user=request.user)
    return render(request, 'interview/dashboard.html', {'profile': profile})
```

```python
# ❌ Bad
from django.shortcuts import *

def dashboard(request):
    p = CandidateProfile.objects.get(user=request.user)
    return render(request, 'interview/dashboard.html', {'profile': p})
```

### Documentation Standards

**Add docstrings to all functions:**

```python
def extract_skills(text):
    """
    Extract technical skills from resume text using spaCy NLP.
    
    Args:
        text (str): The extracted resume text
        
    Returns:
        list: A list of identified skill strings
        
    Example:
        >>> text = "Experienced in Python, Django, and React"
        >>> extract_skills(text)
        ['python', 'django', 'react']
    """
    # Implementation...
```

### Import Order

```python
# 1. Standard library imports
import os
import sys

# 2. Third-party imports
import spacy
from django.shortcuts import render

# 3. Local application imports
from .models import CandidateProfile
from .resume_parser import extract_skills
```

---

## 📝 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

#### Examples:

```bash
# Good commits
feat(resume): add support for .txt file uploads
fix(auth): resolve login redirect loop issue
docs(readme): update installation instructions
refactor(parser): simplify skill extraction logic
test(views): add unit tests for dashboard view

# Bad commits
fixed stuff
update
changes
asdasd
```

### Detailed Commit Example:

```
feat(interview): add skill filtering on dashboard

- Add dropdown filter for skill categories
- Implement AJAX-based filtering without page reload
- Update dashboard template with filter UI
- Add tests for filter functionality

Closes #42
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**
   - Write clean, documented code
   - Follow coding standards
   - Add tests if applicable

3. **Test thoroughly**
   ```bash
   python manage.py test
   python manage.py check
   ```

4. **Commit with clear messages**
   ```bash
   git add .
   git commit -m "feat(parser): add support for .txt resumes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

### Submitting the PR

1. **Open Pull Request** on GitHub
2. **Fill out the PR template:**

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] Added unit tests
- [ ] All tests pass

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
```

3. **Wait for review** - Maintainers will review and provide feedback
4. **Address feedback** - Make requested changes
5. **Merge** - Once approved, your PR will be merged! 🎉

---

## 🐛 Issue Guidelines

### Creating Issues

Use the appropriate issue template:

**Bug Report Template:**
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to...
2. Click on...
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Screenshots**
If applicable

**Environment**
- OS: [e.g., Windows 11]
- Python: [e.g., 3.10.11]
- Django: [e.g., 3.2.25]
```

**Feature Request Template:**
```markdown
**Feature Description**
Clear description of the proposed feature

**Problem it Solves**
What problem does this address?

**Proposed Solution**
How would you implement this?

**Alternatives Considered**
Any alternative approaches?

**Additional Context**
Screenshots, mockups, etc.
```

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `question`: Further information requested
- `wontfix`: Will not be worked on

---

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test interview

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CandidateProfile

class ResumeUploadTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_upload_pdf_resume(self):
        """Test PDF resume upload functionality."""
        self.client.login(username='testuser', password='testpass123')
        
        with open('test_resume.pdf', 'rb') as resume:
            response = self.client.post('/interview/upload/', {
                'resume': resume
            })
            
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            CandidateProfile.objects.filter(user=self.user).exists()
        )
```

---

## 🌟 Recognition

Contributors will be recognized in the following ways:

- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- GitHub contributor badge
- Special shoutouts on social media

---

## 💬 Community

### Communication Channels

- **GitHub Discussions**: For general questions and ideas
- **GitHub Issues**: For bugs and feature requests
- **Discord**: [Join our community](https://discord.gg/nexora)
- **Email**: dev@nexora.ai

### Getting Help

If you need help:
1. Check existing documentation
2. Search existing issues
3. Ask in GitHub Discussions
4. Join our Discord server

---

## 🙏 Thank You!

Your contributions make Nexora better for everyone. Whether you're fixing a typo, adding a feature, or improving documentation, every contribution matters.

### Top Contributors

Check out our amazing contributors on the [Contributors Page](https://github.com/yourusername/nexora/graphs/contributors)!

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [spaCy Documentation](https://spacy.io/usage)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [PEP 8 Style Guide](https://pep8.org/)

---

<div align="center">

**Happy Contributing! 🚀**

Made with ❤️ by the Nexora Community

[⬆ Back to Top](#contributing-to-nexora-)

</div>
