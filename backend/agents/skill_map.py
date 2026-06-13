# ===============================
# GLOBAL SKILL DATABASE
# ===============================

SKILL_DB = [
    "python","java","c++","c","javascript",
    "html","css","react","angular","node",
    "django","flask","spring boot",
    "mysql","mongodb","postgresql","sql",
    "machine learning","deep learning",
    "pandas","numpy","tensorflow","pytorch",
    "docker","kubernetes","aws","azure","gcp",
    "git","linux","rest api",
    "power bi","tableau","excel"
]

# ===============================
# DETECT SKILLS FROM TEXT
# ===============================

def detect_skills_from_text(text):

    if not text:
        return []

    text = text.lower()

    detected_skills = []

    for skill in SKILL_DB:
        if skill in text:
            detected_skills.append(skill)

    return list(set(detected_skills))


# ===============================
# JOB ROLE → REQUIRED SKILLS
# ===============================

JOB_SKILL_MAP = {

    "java developer": [
        "java", "spring boot", "mysql", "rest api", "git"
    ],

    "frontend developer": [
        "html", "css", "javascript", "react", "git"
    ],

    "full stack developer": [
        "html", "css", "javascript",
        "react", "node", "mongodb",
        "sql", "rest api", "git"
    ],

    "data scientist": [
        "python", "machine learning",
        "deep learning", "pandas", "numpy"
    ],

    "data analyst": [
        "excel", "sql", "python",
        "power bi", "tableau"
    ],

    "backend developer": [
        "python", "java",
        "django", "spring boot",
        "mysql", "mongodb",
        "rest api"
    ],

    "web developer": [
        "html", "css", "javascript",
        "react", "mysql"
    ],

    "python developer": [
        "python", "django",
        "flask", "sql",
        "rest api"
    ],

    "machine learning engineer": [
        "python", "machine learning",
        "tensorflow", "pytorch",
        "pandas", "numpy"
    ],

    "devops engineer": [
        "docker", "kubernetes",
        "aws", "linux",
        "git"
    ],

    "cloud engineer": [
        "aws", "azure",
        "gcp", "linux",
        "docker"
    ],

    "mobile app developer": [
        "java", "kotlin",
        "firebase"
    ],

    "android developer": [
        "java", "kotlin",
        "android studio",
        "firebase", "rest api"
    ],

    "ios developer": [
        "swift",
        "xcode",
        "ios sdk"
    ],

    "software tester": [
        "manual testing",
        "selenium",
        "test cases",
        "automation testing"
    ],

    "qa engineer": [
        "manual testing",
        "automation testing",
        "selenium",
        "jira"
    ],

    "ui ux designer": [
        "figma",
        "adobe xd",
        "wireframing",
        "prototyping"
    ],

    "cyber security analyst": [
        "network security",
        "penetration testing",
        "ethical hacking"
    ],

    "database administrator": [
        "sql",
        "mysql",
        "postgresql",
        "database design"
    ]
}


# ===============================
# ROLE CATEGORY KEYWORDS
# ===============================

ROLE_KEYWORDS = {

    "ai": ["python","machine learning","deep learning","tensorflow","pytorch"],

    "data": ["python","pandas","numpy","sql","machine learning"],

    "cloud": ["aws","azure","gcp","docker","kubernetes"],

    "devops": ["docker","kubernetes","aws","linux","git"],

    "frontend": ["html","css","javascript","react"],

    "backend": ["python","django","flask","rest api","sql"],

    "mobile": ["java","kotlin","firebase"],

    "android": ["java","kotlin","android studio","firebase"],

    "ios": ["swift","xcode","ios sdk"],

    "security": ["network security","ethical hacking","penetration testing"]
}


# ===============================
# SKILL LEARNING LINKS
# ===============================

SKILL_LEARNING_LINKS = {

    "python": "https://www.w3schools.com/python/",
    "java": "https://www.w3schools.com/java/",
    "html": "https://www.w3schools.com/html/",
    "css": "https://www.w3schools.com/css/",
    "javascript": "https://www.w3schools.com/js/",
    "react": "https://react.dev/learn",
    "node": "https://nodejs.org/en/learn",
    "mongodb": "https://www.mongodb.com/docs/",
    "sql": "https://www.w3schools.com/sql/",
    "django": "https://docs.djangoproject.com/en/stable/",
    "flask": "https://flask.palletsprojects.com/",
    "machine learning": "https://www.coursera.org/learn/machine-learning",
    "deep learning": "https://www.deeplearning.ai/",
    "pandas": "https://pandas.pydata.org/docs/",
    "numpy": "https://numpy.org/doc/",
    "docker": "https://docs.docker.com/get-started/",
    "kubernetes": "https://kubernetes.io/docs/tutorials/",
    "aws": "https://aws.amazon.com/getting-started/",
    "linux": "https://linuxjourney.com/",
    "git": "https://git-scm.com/docs/gittutorial"
}


# ===============================
# GET SKILLS FROM ROLE
# ===============================

def get_skills_from_role(role_name):

    if not role_name:
        return []

    role_name = role_name.lower().strip()

    # Exact role match
    if role_name in JOB_SKILL_MAP:
        return JOB_SKILL_MAP[role_name]

    detected = []

    # Detect skills from text
    for skill in SKILL_DB:
        if skill in role_name:
            detected.append(skill)

    # Detect role category
    for key, skills in ROLE_KEYWORDS.items():
        if key in role_name:
            detected.extend(skills)

    return list(set(detected))


# ===============================
# GET LEARNING LINKS
# ===============================

def get_learning_links(missing_skills):

    links = []

    for skill in missing_skills:
        if skill in SKILL_LEARNING_LINKS:
            links.append({
                "skill": skill,
                "link": SKILL_LEARNING_LINKS[skill]
            })

    return links