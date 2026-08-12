import re


SKILLS = [

    # Programming
    "python",
    "java",
    "c++",
    "javascript",

    # Machine Learning
    "machine learning",
    "deep learning",
    "scikit-learn",
    "tensorflow",
    "pytorch",

    # AI / NLP
    "artificial intelligence",
    "natural language processing",
    "nlp",
    "computer vision",
    "generative ai",
    "genai",
    "llm",
    "large language model",
    "rag",
    "retrieval augmented generation",

    # Frameworks
    "django",
    "flask",
    "fastapi",
    "langchain",

    # Data
    "numpy",
    "pandas",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    # Cloud / DevOps
    "aws",
    "azure",
    "docker",
    "git",
    "github",

]


def normalize_text(text):

    return text.lower()


def extract_skills(text):

    text = normalize_text(text)

    found_skills = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            found_skills.append(skill)

    return sorted(set(found_skills))


def compare_skills(jd_text, resume_text):

    jd_skills = set(
        extract_skills(jd_text)
    )

    resume_skills = set(
        extract_skills(resume_text)
    )

    matched_skills = sorted(
        jd_skills.intersection(resume_skills)
    )

    missing_skills = sorted(
        jd_skills.difference(resume_skills)
    )

    if len(jd_skills) == 0:

        skill_score = 100

    else:

        skill_score = (
            len(matched_skills)
            / len(jd_skills)
        ) * 100

    return {
        "jd_skills": sorted(jd_skills),
        "resume_skills": sorted(resume_skills),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_score": round(skill_score, 2)
    }