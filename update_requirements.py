#!/usr/bin/env python
"""
Auto-update requirements.txt with currently installed packages
Usage: python update_requirements.py
"""

import subprocess
import sys
from datetime import datetime


def update_requirements():
    """Update requirements.txt with all installed packages"""
    
    print("🔍 Scanning installed packages...")
    
    # Get all installed packages
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True,
        text=True,
        check=True
    )
    
    packages = result.stdout.strip().split('\n')
    
    # Filter out local packages and editable installs
    filtered_packages = []
    for pkg in packages:
        if pkg and not pkg.startswith('-e') and not pkg.startswith('#'):
            # Skip the spacy model (it's not a regular package)
            if 'en_core_web_sm' not in pkg:
                filtered_packages.append(pkg)
    
    # Create header
    header = f"""# ============================================
# Nexora - InterviewPrepAI Requirements
# Python 3.10+
# Auto-generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# ============================================

# Core Dependencies (manually organized)
# Run: pip install -r requirements.txt
# Then: python -m spacy download en_core_web_sm

"""
    
    # Categorize packages
    core = ['Django', 'djongo', 'pymongo', 'sqlparse', 'asgiref', 'pytz']
    parsing = ['pdfplumber', 'python-docx', 'pdfminer.six', 'pypdfium2', 'pillow', 'lxml']
    nlp = ['spacy', 'spacy-legacy', 'spacy-loggers', 'thinc', 'blis', 'cymem', 
           'murmurhash', 'preshed', 'wasabi', 'srsly', 'catalogue', 'typer',
           'confection', 'pydantic', 'pydantic_core', 'langcodes', 'language_data',
           'weasel', 'cloudpathlib']
    
    categorized = []
    other = []
    
    for pkg in filtered_packages:
        pkg_name = pkg.split('==')[0].replace('_', '-')
        if any(c.lower() in pkg_name.lower() for c in core):
            categorized.append(('Core Framework', pkg))
        elif any(p.lower() in pkg_name.lower() for p in parsing):
            categorized.append(('Resume Parsing', pkg))
        elif any(n.lower() in pkg_name.lower() for n in nlp):
            categorized.append(('NLP & AI', pkg))
        else:
            other.append(pkg)
    
    # Write to requirements.txt
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(header)
        
        # Write categorized packages
        current_category = None
        for category, pkg in sorted(categorized):
            if category != current_category:
                f.write(f"\n# ==================== {category} ====================\n")
                current_category = category
            f.write(f"{pkg}\n")
        
        # Write other packages
        if other:
            f.write("\n# ==================== Other Dependencies ====================\n")
            for pkg in sorted(other):
                f.write(f"{pkg}\n")
        
        # Add development section
        f.write("\n# ==================== Development (Optional) ====================\n")
        f.write("# Uncomment these for development:\n")
        f.write("# pytest==7.4.3             # Testing framework\n")
        f.write("# pytest-django==4.7.0      # Django testing plugin\n")
        f.write("# coverage==7.3.2           # Code coverage\n")
        f.write("# black==23.11.0            # Code formatter\n")
        f.write("# flake8==6.1.0             # Linting\n")
    
    print(f"✅ requirements.txt updated with {len(filtered_packages)} packages")
    print(f"📦 Total size: {len(result.stdout)} bytes")
    print("\n📝 Remember to:")
    print("   1. Review the generated file")
    print("   2. Test with: pip install -r requirements.txt")
    print("   3. Download spaCy model: python -m spacy download en_core_web_sm")


if __name__ == "__main__":
    try:
        update_requirements()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
