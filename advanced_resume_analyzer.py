import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# =========================
# APP SETTINGS
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =========================
# ROLE DATABASE
# =========================

roles = {
    "Python Developer": {
        "skills": ["python", "sql", "flask", "django", "api", "oops", "git"],
        "learn": [
            "Machine Learning",
            "Data Structures",
            "Automation",
            "Advanced Python"
        ]
    },

    "Java Developer": {
        "skills": [
            "java",
            "spring boot",
            "jdbc",
            "sql",
            "hibernate",
            "oops",
            "collections"
        ],
        "learn": [
            "Microservices",
            "Spring Security",
            "System Design"
        ]
    },

    "Frontend Developer": {
        "skills": [
            "html",
            "css",
            "javascript",
            "react",
            "bootstrap",
            "ui",
            "responsive design"
        ],
        "learn": [
            "React Projects",
            "Animations",
            "UI/UX"
        ]
    },

    "Backend Developer": {
        "skills": [
            "java",
            "python",
            "sql",
            "api",
            "mongodb",
            "nodejs"
        ],
        "learn": [
            "REST APIs",
            "Cloud",
            "Database Optimization"
        ]
    },

    "Full Stack Developer": {
        "skills": [
            "html",
            "css",
            "javascript",
            "react",
            "java",
            "spring boot",
            "sql"
        ],
        "learn": [
            "Deployment",
            "Cloud Hosting",
            "Frontend + Backend Integration"
        ]
    }
}

# =========================
# JOB DATABASE
# =========================

jobs = {
    "Python Developer": [
        "Django Developer",
        "Backend Engineer",
        "Automation Engineer",
        "Data Engineer"
    ],

    "Java Developer": [
        "Spring Boot Developer",
        "Backend Java Developer",
        "Software Engineer"
    ],

    "Frontend Developer": [
        "React Developer",
        "UI Developer",
        "Web Designer"
    ],

    "Backend Developer": [
        "API Developer",
        "Node.js Developer",
        "System Engineer"
    ],

    "Full Stack Developer": [
        "Full Stack Engineer",
        "MERN Developer",
        "Software Engineer"
    ]
}

last_result = {}

# =========================
# FUNCTIONS
# =========================

def browse_pdf():
    file = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]
    )

    if file:
        pdf_entry.delete(0, "end")
        pdf_entry.insert(0, file)


def analyze_resume():
    global last_result

    result_box.delete("1.0", "end")

    try:
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        role = role_menu.get()
        pdf_path = pdf_entry.get().strip()

        if not name or not email or not pdf_path:
            messagebox.showerror(
                "Error",
                "Please fill all fields and select a PDF."
            )
            return

        reader = PdfReader(pdf_path)

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

        progress["value"] = score

        if score >= 80:
            status = "Excellent Resume"
        elif score >= 50:
            status = "Good Resume"
        else:
            status = "Needs Improvement"

        last_result = {
            "name": name,
            "email": email,
            "role": role,
            "required": required_skills,
            "matched": matched,
            "missing": missing,
            "score": score,
            "status": status
        }

        result_box.insert("end", "===== AI RESUME ANALYSIS =====\n\n")
        result_box.insert("end", f"Name : {name}\n")
        result_box.insert("end", f"Email : {email}\n")
        result_box.insert("end", f"Role : {role}\n\n")

        result_box.insert(
            "end",
            f"Total Skills Required : {len(required_skills)}\n\n"
        )

        result_box.insert("end", "===== REQUIRED SKILLS =====\n")

        for skill in required_skills:
            result_box.insert("end", f"• {skill}\n")

        result_box.insert("end", "\n===== MATCHED SKILLS =====\n")

        for skill in matched:
            result_box.insert("end", f"✔ {skill}\n")

        result_box.insert(
            "end",
            f"\nMatched Skills : {len(matched)}/{len(required_skills)}\n"
        )

        result_box.insert("end", "\n===== MISSING SKILLS =====\n")

        for skill in missing:
            result_box.insert("end", f"✘ {skill}\n")

        result_box.insert(
            "end",
            f"\nMissing Skills : {len(missing)}/{len(required_skills)}\n"
        )

        result_box.insert(
            "end",
            f"\nResume Match Percentage : {score:.2f}%\n"
        )

        result_box.insert(
            "end",
            f"Status : {status}\n"
        )

        result_box.insert(
            "end",
            "\n===== LEARNING ROADMAP =====\n"
        )

        for item in roles[role]["learn"]:
            result_box.insert("end", f"📘 {item}\n")

        result_box.insert(
            "end",
            "\n===== JOB RECOMMENDATIONS =====\n"
        )

        for job in jobs[role]:
            result_box.insert("end", f"💼 {job}\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def download_pdf():
    if not last_result:
        messagebox.showwarning(
            "Warning",
            "Analyze Resume First"
        )
        return

    file = filedialog.asksaveasfilename(
        defaultextension=".pdf"
    )

    if not file:
        return

    c = canvas.Canvas(file, pagesize=A4)

    y = 800

    c.setFont("Helvetica-Bold", 18)
    c.drawString(150, y, "AI Resume Analysis Report")

    y -= 40

    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Name : {last_result['name']}")
    y -= 20

    c.drawString(50, y, f"Email : {last_result['email']}")
    y -= 20

    c.drawString(50, y, f"Role : {last_result['role']}")
    y -= 20

    c.drawString(
        50,
        y,
        f"Score : {last_result['score']:.2f}%"
    )
    y -= 20

    c.drawString(
        50,
        y,
        f"Status : {last_result['status']}"
    )

    c.save()

    messagebox.showinfo(
        "Success",
        "PDF Report Generated Successfully"
    )

# =========================
# UI
# =========================

app = ctk.CTk()

app.geometry("1100x800")
app.title("AI Resume Analyzer - By Farhath")

ctk.CTkLabel(
    app,
    text="AI Resume Analyzer & Career System",
    font=("Arial", 30, "bold")
).pack(pady=10)

ctk.CTkLabel(
    app,
    text="- Developed by Farhath",
    font=("Arial", 18)
).pack()

name_entry = ctk.CTkEntry(
    app,
    width=500,
    placeholder_text="Name"
)
name_entry.pack(pady=10)

email_entry = ctk.CTkEntry(
    app,
    width=500,
    placeholder_text="Email"
)
email_entry.pack(pady=10)

role_menu = ctk.CTkOptionMenu(
    app,
    values=list(roles.keys())
)
role_menu.pack(pady=10)

pdf_entry = ctk.CTkEntry(
    app,
    width=500,
    placeholder_text="Select Resume PDF"
)
pdf_entry.pack(pady=10)

ctk.CTkButton(
    app,
    text="Browse PDF",
    command=browse_pdf
).pack(pady=5)

ctk.CTkButton(
    app,
    text="Analyze Resume",
    command=analyze_resume
).pack(pady=10)

progress = Progressbar(
    app,
    length=400,
    mode="determinate"
)
progress.pack(pady=10)

ctk.CTkButton(
    app,
    text="Download PDF Report",
    command=download_pdf
).pack(pady=10)

result_box = ctk.CTkTextbox(
    app,
    width=950,
    height=350
)
result_box.pack(pady=20)

app.mainloop()

