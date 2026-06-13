from agents.skill_map import JOB_SKILL_MAP

def get_trained_job_skills(job_title):
    if not job_title:
        return None

    job_title = job_title.lower()

    for role, skills in JOB_SKILL_MAP.items():
        if role in job_title:
            return skills

    return None
