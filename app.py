import io
import os
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

# ================= ADMIN =================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password" #create your password

# ================= EMAIL CONFIG =================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "trivenip.softwaredeveloper@gmail.com"  # Replace with your mail
app.config['MAIL_PASSWORD'] = "duwe utgl mifm upfm" #Replace with password

mail = Mail(app)

# ================= MONGODB CONFIG (FIXED) =================
client = MongoClient(
    "mongodb+srv://skillgapuser:skillgap123@cluster0.vloq8ub.mongodb.net/?appName=Cluster0",#set your mongo url
    tls=True,
    tlsCAFile=certifi.where()
)

db = client["skillgapdb"]
users = db["users"]
fs = gridfs.GridFS(db)

print("✅ MongoDB Connected Successfully")

# ================= EMAIL FUNCTION =================
def send_result_email(to, name, status, missing_skills, match_percentage):

    print("📧 Sending email to:", to)

    body = f"""
Hi {name},

Thank you for using the Skill Gap Analyzer Tool.

Here is your detailed Skill Compatibility Report:

-------------------------------------------------
Overall Match Score : {match_percentage}%
Assessment Level    : {status}
-------------------------------------------------
"""

    if missing_skills:

        body += f"""

Identified Skill Gaps:
{', '.join(missing_skills)}

Recommendation:
To improve your chances for this role, focus on these skills.

• Work on real projects
• Take certification courses
• Practice coding platforms
• Improve your resume with achievements
"""

        # Get learning links
        learning_links = get_learning_links(missing_skills)

        if learning_links:

            body += "\n\nRecommended Learning Resources\n"

            for item in learning_links:
                body += f"\n• {item['skill'].title()}\n{item['link']}\n"

    else:

        body += """

Excellent Work!

Your profile strongly aligns with the required skills.
You are well prepared for this role.
"""

    body += """

-------------------------------------------------
This report is generated for analytical and career development purposes only.

Regards,
Skill Gap Analyzer Team
"""

    msg = Message(
        subject="Skill Compatibility Report",
        sender=app.config['MAIL_USERNAME'],
        recipients=[to]
    )

    msg.body = body
    mail.send(msg)

    print("✅ Email Sent Successfully")

# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")

# ================= ANALYZE =================
@app.route("/analyze", methods=["POST"])
def analyze():

    name = request.form["name"]
    email = request.form["email"]
    job_description = request.form.get("job_description", "").lower().strip()
    resume_file = request.files["resume_file"]

    # Save to GridFS
    file_id = fs.put(
        resume_file.read(),
        filename=resume_file.filename,
        contentType="application/pdf"
    )

    # Save locally
    resume_path = os.path.join(app.config["UPLOAD_FOLDER"], resume_file.filename)
    resume_file.seek(0)
    resume_file.save(resume_path)

    # Extract skills
    resume_skills = get_resume_skills(resume_path) or []
    job_skills = get_skills_from_role(job_description) or []

    matched_skills = list(set(job_skills) & set(resume_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    match_percentage = round((len(matched_skills) / len(job_skills)) * 100) if job_skills else 0

    if match_percentage >= 80:
        status = "Excellent Match"
    elif match_percentage >= 60:
        status = "Good Match"
    elif match_percentage >= 40:
        status = "Moderate Match"
    else:
        status = "Skill Gap Detected"

    # Save to MongoDB
    users.insert_one({
        "name": name,
        "email": email,
        "job_description": job_description,
        "resume_file_id": file_id,
        "resume_filename": resume_file.filename,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
        "status": status
    })

    # Send email safely
    try:
    #send_result_email(email, name, status, missing_skills, match_percentage)
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

# ================= ADMIN LOGIN =================
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))
        return "Invalid Credentials"

    return render_template("admin_login.html")

# ================= ADMIN DASHBOARD =================
@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    all_users = list(users.find())
    return render_template("admin.html", users=all_users)

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin_login"))

# ================= DOWNLOAD RESUME =================
@app.route("/resume/<file_id>")
def download_resume(file_id):

    file = fs.get(ObjectId(file_id))
    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    with open(path, "wb") as f:
        f.write(file.read())

    return send_file(path, as_attachment=True)

# ================= GRAPH =================
@app.route("/view-graph")
def view_graph():

    return render_template(
        "graph.html",
        percentage=int(request.args.get("percentage", 0)),
        matched_count=int(request.args.get("matched", 0)),
        missing_count=int(request.args.get("missing", 0))
    )

# ================= REPORT DOWNLOAD =================
@app.route("/download-report")
def download_report():

    report = f"""
SKILL GAP ANALYZER REPORT
==========================
Name: {request.args.get('name')}
Email: {request.args.get('email')}
Role: {request.args.get('role')}
Score: {request.args.get('percentage')}%
==========================
"""

    return send_file(
        io.BytesIO(report.encode()),
        mimetype="text/plain",
        as_attachment=True,
        download_name="report.txt"
    )

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)