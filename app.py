import io
import os
from dotenv import load_dotenv
load_dotenv()

import gridfs
import certifi
from bson import ObjectId
from flask import Flask, render_template, request, send_file, redirect, url_for, session
from flask_mail import Mail, Message
from pymongo import MongoClient

from agents.resume_agent import get_resume_skills
from agents.skill_map import get_skills_from_role, get_learning_links


# ================= FLASK CONFIG =================
app = Flask(__name__)
app.secret_key = "skillgapsecret"

app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

print("APP STARTED")

# ================= ADMIN =================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

# ================= EMAIL CONFIG =================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

print("MAIL_USERNAME =", app.config["MAIL_USERNAME"])
print("MAIL_PASSWORD EXISTS =", bool(app.config["MAIL_PASSWORD"]))

mail = Mail(app)

# ================= MONGODB CONFIG =================
MONGO_URI = os.getenv("MONGO_URI")

print("MONGO_URI =", MONGO_URI)

if not MONGO_URI:
    raise Exception("MONGO_URI not found in environment variables")

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client["skillgapdb"]
users = db["users"]

print("MongoDB Connected Successfully")


# ================= EMAIL FUNCTION =================
def send_result_email(to, name, status, missing_skills, match_percentage):

    print("📧 Sending email to:", to)

    body = f"""
Hi {name},

Thank you for using Skill Gap Analyzer.

Score: {match_percentage}%
Status: {status}

Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}

Regards,
Skill Gap Analyzer Team
"""

    msg = Message(
        subject="Skill Gap Report",
        sender=app.config['MAIL_USERNAME'],
        recipients=[to]
    )

    msg.body = body
    mail.send(msg)

    print("Email sent successfully")


# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")


# ================= TEST EMAIL =================
@app.route("/test-email")
def test_email():

    msg = Message(
        "Test Email",
        sender=app.config["MAIL_USERNAME"],
        recipients=[app.config["MAIL_USERNAME"]]
    )

    msg.body = "Testing Flask Mail"

    mail.send(msg)

    return "Email Sent Successfully"


# ================= ANALYZE =================
@app.route("/analyze", methods=["POST"])
def analyze():

    name = request.form["name"]
    email = request.form["email"]
    job_description = request.form.get("job_description", "").lower().strip()
    resume_file = request.files["resume_file"]

    file_id = None

    resume_path = os.path.join(app.config["UPLOAD_FOLDER"], resume_file.filename)
    resume_file.save(resume_path)

    resume_skills = get_resume_skills(resume_path) or []
    job_skills = get_skills_from_role(job_description) or []

    matched_skills = list(set(job_skills) & set(resume_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    if job_skills:
        match_percentage = round((len(matched_skills) / len(job_skills)) * 100)
    else:
        match_percentage = 0

    if match_percentage >= 80:
        status = "Excellent Match"
    elif match_percentage >= 60:
        status = "Good Match"
    elif match_percentage >= 40:
        status = "Moderate Match"
    else:
        status = "Skill Gap Detected"

    users.insert_one({
        "name": name,
        "email": email,
        "job_description": job_description,
        "resume_filename": resume_file.filename,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
        "status": status
    })

    # EMAIL SAFE CALL
    try:
        send_result_email(
            email,
            name,
            status,
            missing_skills,
            match_percentage
        )
    except Exception as e:
        print("Email error:", e)

    return render_template(
        "result.html",
        name=name,
        email=email,
        role=job_description,
        percentage=match_percentage,
        status=status,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        job_skills=job_skills
    )
    @app.route("/mail-debug")
def mail_debug():

    print("MAIL USER:", app.config["MAIL_USERNAME"])
    print("MAIL PASS EXISTS:", bool(app.config["MAIL_PASSWORD"]))

    return f"""
    USER: {app.config["MAIL_USERNAME"]}<br>
    PASS EXISTS: {bool(app.config["MAIL_PASSWORD"])}
    """


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)