# backend/agents/resume_agent.py

import pdfplumber

# AI skill list
ALL_SKILLS = [
    "python","java","javascript","html","css","react","node","mongodb","sql",
    "flask","django","express","git","github","aws","docker","linux",
    "machine learning","data science","nlp","tensorflow","keras",
    "api","rest","bootstrap","tailwind","figma","c++","php","mysql",
    "postman","firebase","redux","vue","angular"
]

def get_resume_skills(pdf_path):

    text = ""

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                content = page.extract_text()

                if content:
                    text += content.lower()

    except Exception as e:

        print("❌ PDF Reading Error:", e)

        return []

    found_skills = []

    for skill in ALL_SKILLS:

        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))