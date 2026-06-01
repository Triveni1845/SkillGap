# AI Resume Skill Gap Analyzer

## Overview

The **AI Resume Skill Gap Analyzer** is a web-based application designed to analyze a candidate's resume and compare it with the **skills required for a specific job role**.

The system identifies **skill gaps** by comparing the candidate's existing skills with industry-required skills. It also recommends **learning resources** to help users improve their missing skills.

This project demonstrates the use of **Python, Flask, and MongoDB** to build an intelligent tool that assists users in understanding their **career readiness for a target job role**.

---

## Key Features

* Upload resume in **PDF format**
* **Automatic skill extraction** from the uploaded resume
* **Job role based skill mapping**
* **Skill gap detection**
* **Skill match percentage calculation**
* **Learning resource recommendations** for missing skills
* **Email notification** with analysis results
* **Admin dashboard** to view user submissions
* Clean and simple **web interface**

---

## Technology Stack

### Backend

* **Python**
* **Flask**

### Database

* **MongoDB Atlas**
* **GridFS** (for storing resumes)

### Frontend

* **HTML**
* **CSS**
* **JavaScript**

### Additional Libraries

* Flask-Mail
* PyMongo
* GridFS

---

## Project Structure

```
SkillGapAnalyzer
│
├── backend
│   ├── app.py
│   │
│   └── agents
│       ├── resume_agent.py
│       └── skill_map.py
│
├── templates
│   ├── index.html
│   ├── result.html
│   ├── admin.html
│   └── admin_login.html
│
├── static
│   ├── css
│   └── js
│
├── uploads
│
└── README.md
```

---

## Important Files

### `app.py`

Main Flask application that handles:

* Resume upload
* Skill comparison
* Result generation
* Email sending
* Admin dashboard

### `resume_agent.py`

Responsible for **extracting skills from the uploaded resume**.

### `skill_map.py`

Contains:

* Job role to skill mapping
* Skill database
* Learning resource links

---

## How the System Works

1. The user uploads a **resume in PDF format**.
2. The system extracts **skills from the resume**.
3. The user enters a **target job role**.
4. The system retrieves **required skills for the role**.
5. The system compares:

   * Resume skills
   * Required job skills
6. A **match percentage** is calculated.
7. **Missing skills** are identified.
8. The system recommends **learning resources** for improvement.
9. The result is displayed on the screen and sent via **email**.

---

## Installation and Setup

### 1. Clone the Repository

```
git clone https://github.com/yourusername/AI-Resume-Skill-Gap-Analyzer.git
```

### 2. Navigate to the Project Folder

```
cd AI-Resume-Skill-Gap-Analyzer/backend
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Configure MongoDB

Update the **MongoDB connection string** in `app.py` with your MongoDB Atlas URI.

### 5. Configure Email

Update the following fields in `app.py`:

```
MAIL_USERNAME
MAIL_PASSWORD
```

Use a **Gmail App Password** for secure email sending.

### 6. Run the Application

```
python app.py
```

### 7. Open the Application

```
http://127.0.0.1:5000
```

---

## Example

### Resume Skills

* Python
* SQL
* Git

### Required Skills for Python Developer

* Python
* Django
* Flask
* SQL
* REST API

### Missing Skills

* Django
* Flask
* REST API

The system also provides **learning links** to help the user acquire these skills.

---

## Future Enhancements

* Advanced **AI-based resume parsing**
* **Graph visualization** of skill matching
* Integration with **job portals**
* Improved **skill recommendation system**
* Enhanced **admin analytics dashboard**

---

## Author

Developed as an academic project to demonstrate **AI-based resume analysis and skill gap detection** using modern web technologies.

---

## License

This project is open-source and intended for **educational and learning purposes**.
