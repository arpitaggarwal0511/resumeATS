# server/ats_score.py
import re

def compute_ats_score(text: str, extracted_sections: list[str]) -> int:
    score = 0
    max_score = 100

    # --- 1. Section Presence Check ---
    expected_sections = [
        "Contact Information", "Education", "Experience", "Projects", 
        "Technical Skills", "Certifications", "Achievements", "Publications"
    ]
    section_weight = 20
    found_sections = [sec for sec in expected_sections if sec in extracted_sections]
    score += section_weight * len(found_sections) / len(expected_sections)

    # --- 2. Format & Contact Check ---
    format_score = 0
    if re.search(r'\b\d{10}\b|\+\d{1,3}\s?\d{10}\b', text):
        format_score += 5  # phone number
    if re.search(r'[\w\.-]+@[\w\.-]+', text):
        format_score += 5  # email
    if "linkedin.com" in text.lower():
        format_score += 5  # LinkedIn
    if "github.com" in text.lower():
        format_score += 5  # GitHub or portfolio
    score += format_score  # Max 20

    # --- 3. Keyword Matching ---
    keywords = [
        # Programming languages
        "python", "java", "c++", "c", "typescript", "javascript", "go", "ruby", "kotlin", "rust",
        # Web development
        "react", "nextjs", "nodejs", "express", "html", "css", "tailwind", "redux",
        # Backend & APIs
        "rest", "graphql", "flask", "django", "fastapi",
        # Databases
        "sql", "mysql", "postgresql", "mongodb", "firebase", "nosql",
        # DevOps
        "aws", "gcp", "azure", "docker", "kubernetes", "jenkins", "terraform", "ci/cd",
        # Data Science & ML
        "machine learning", "deep learning", "pandas", "numpy", "matplotlib", "seaborn", 
        "scikit-learn", "tensorflow", "keras", "pytorch", "huggingface", "nlp", 
        "data analysis", "data visualization", "big data",
        # Tools
        "git", "github", "jira", "linux", "bash", "shell scripting",
        # Roles (contextual keywords)
        "sde", "software engineer", "data scientist", "data analyst", 
        "ml engineer", "devops engineer", "site reliability engineer", "backend engineer"
    ]

    keyword_score = 0
    for kw in keywords:
        if kw.lower() in text.lower():
            keyword_score += 1.5  # each keyword is 1.5 pt
    score += min(keyword_score, 40)  # Cap keyword score at 40

    # --- 4. Resume Length Check ---
    word_count = len(text.split())
    if 300 <= word_count <= 1200:
        score += 10  # Ideal length
    elif word_count > 1200:
        score += 5   # Acceptable but long
    # else too short — no score

    return min(int(score), max_score)
