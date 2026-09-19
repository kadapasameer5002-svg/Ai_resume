from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

# =========================
# ROLE DATABASE
# =========================

roles = {
    "Python Developer": {
        "skills": ["python", "sql", "flask", "django", "api", "oops", "git"],
        "learn": ["Machine Learning", "Data Structures", "Automation", "Advanced Python"]
    },
    "Java Developer": {
        "skills": ["java", "spring boot", "jdbc", "sql", "hibernate", "oops", "collections"],
        "learn": ["Microservices", "Spring Security", "System Design"]
    },
    "Frontend Developer": {
        "skills": ["html", "css", "javascript", "react", "bootstrap", "ui", "responsive design"],
        "learn": ["React Projects", "Animations", "UI/UX"]
    },
    "Backend Developer": {
        "skills": ["java", "python", "sql", "api", "mongodb", "nodejs"],
        "learn": ["REST APIs", "Cloud", "Database Optimization"]
    },
    "Full Stack Developer": {
        "skills": ["html", "css", "javascript", "react", "java", "spring boot", "sql"],
        "learn": ["Deployment", "Cloud Hosting", "Frontend + Backend Integration"]
    }
}

# =========================
# JOB DATABASE
# =========================

jobs = {
    "Python Developer": ["Django Developer", "Backend Engineer", "Automation Engineer", "Data Engineer"],
    "Java Developer": ["Spring Boot Developer", "Backend Java Developer", "Software Engineer"],
    "Frontend Developer": ["React Developer", "UI Developer", "Web Designer"],
    "Backend Developer": ["API Developer", "Node.js Developer", "System Engineer"],
    "Full Stack Developer": ["Full Stack Engineer", "MERN Developer", "Software Engineer"]
}

def analyze_resume(name, email, role, pdf_file_stream):
    """
    Analyzes a resume PDF and returns a structured dictionary of results.
    """
    if role not in roles:
        raise ValueError("Invalid role selected")
        
    reader = PdfReader(pdf_file_stream)
    resume_text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            resume_text += page_text.lower()

    required_skills = roles[role]["skills"]
    matched = []
    missing = []

    for skill in required_skills:
        if skill.lower() in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    score = (len(matched) / len(required_skills)) * 100

    if score >= 80:
        status = "Excellent Resume"
    elif score >= 50:
        status = "Good Resume"
    else:
        status = "Needs Improvement"

    result = {
        "name": name,
        "email": email,
        "role": role,
        "required": required_skills,
        "matched": matched,
        "missing": missing,
        "score": round(score, 2),
        "status": status,
        "learning_roadmap": roles[role]["learn"],
        "job_recommendations": jobs[role]
    }
    
    return result

def generate_pdf_report(result_data):
    """
    Generates a PDF report as bytes based on the analysis results.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    y = 800

    c.setFont("Helvetica-Bold", 18)
    c.drawString(150, y, "AI Resume Analysis Report")
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Name : {result_data['name']}")
    y -= 20
    c.drawString(50, y, f"Email : {result_data['email']}")
    y -= 20
    c.drawString(50, y, f"Role : {result_data['role']}")
    y -= 20
    c.drawString(50, y, f"Score : {result_data['score']:.2f}%")
    y -= 20
    c.drawString(50, y, f"Status : {result_data['status']}")

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
