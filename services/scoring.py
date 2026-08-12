import re

from .similarity import calculate_similarity
from .skill_extractor import compare_skills


def extract_experience(text):

    text = text.lower()

    pattern = (
        r"(\d+(?:\.\d+)?)"
        r"\+?\s+years?\s+"
        r"(?:of\s+)?experience"
    )

    matches = re.findall(
        pattern,
        text
    )

    if not matches:

        return 0.0

    values = []

    for value in matches:

        try:

            values.append(
                float(value)
            )

        except ValueError:

            pass

    return max(values, default=0.0)


def calculate_experience_score(
    jd_text,
    resume_text
):

    required_experience = extract_experience(
        jd_text
    )

    candidate_experience = extract_experience(
        resume_text
    )

    if required_experience == 0:

        return {
            "required_experience": 0,
            "candidate_experience": candidate_experience,
            "experience_score": 100
        }

    score = (
        candidate_experience
        / required_experience
    ) * 100

    score = min(score, 100)

    return {
        "required_experience": required_experience,
        "candidate_experience": candidate_experience,
        "experience_score": round(score, 2)
    }


def education_score(jd_text, resume_text):

    education_keywords = [

        "bachelor",
        "b.tech",
        "b.e",
        "b.e.",
        "m.tech",
        "m.e",
        "master",
        "computer science",
        "information technology",
        "electronics",
        "artificial intelligence",
        "data science"

    ]

    jd_lower = jd_text.lower()
    resume_lower = resume_text.lower()

    jd_requires_education = any(
        keyword in jd_lower
        for keyword in education_keywords
    )

    if not jd_requires_education:

        return 100

    candidate_has_education = any(
        keyword in resume_lower
        for keyword in education_keywords
    )

    if candidate_has_education:

        return 100

    return 40


def generate_recommendation(score):

    if score >= 85:

        return "Strongly Recommended"

    elif score >= 75:

        return "Recommended"

    elif score >= 60:

        return "Consider"

    else:

        return "Not Recommended"


def calculate_final_score(
    jd_text,
    resume_text
):

    # NLP similarity
    similarity_score = calculate_similarity(
        jd_text,
        resume_text
    )

    # Skill matching
    skill_result = compare_skills(
        jd_text,
        resume_text
    )

    # Experience
    experience_result = calculate_experience_score(
        jd_text,
        resume_text
    )

    # Education
    edu_score = education_score(
        jd_text,
        resume_text
    )

    # Weighted score
    final_score = (

        similarity_score * 0.50

        + skill_result["skill_score"] * 0.30

        + experience_result["experience_score"] * 0.10

        + edu_score * 0.10

    )

    final_score = round(
        final_score,
        2
    )

    recommendation = generate_recommendation(
        final_score
    )

    return {

        "final_score": final_score,

        "similarity_score":
            similarity_score,

        "skill_score":
            skill_result["skill_score"],

        "experience_score":
            experience_result["experience_score"],

        "education_score":
            edu_score,

        "matched_skills":
            skill_result["matched_skills"],

        "missing_skills":
            skill_result["missing_skills"],

        "jd_skills":
            skill_result["jd_skills"],

        "resume_skills":
            skill_result["resume_skills"],

        "required_experience":
            experience_result["required_experience"],

        "candidate_experience":
            experience_result["candidate_experience"],

        "recommendation":
            recommendation

    } 