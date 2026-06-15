import os
import google.generativeai as genai

api_key = os.getenv("GOOGLE_API_KEY")

print("API key found:", bool(api_key))
print("API key length:", len(api_key) if api_key else 0)

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def get_skills_from_gemini(job_role):
    prompt = f"""
    List the technical skills required for the job role: {job_role}

    Return only a comma separated list.
    Example:
    Python, Flask, SQL, MongoDB, Git
    """

    response = model.generate_content(prompt)

    skills = [
        skill.strip().lower()
        for skill in response.text.split(",")
        if skill.strip()
    ]

    return skills