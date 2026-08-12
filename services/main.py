from .parser import read_text_file
from .scoring import calculate_final_score 


# -----------------------------------
# 1. File paths
# -----------------------------------

JD_PATH = "data/job_description.txt"

RESUME_PATH = "data/resume.txt"


# -----------------------------------
# 2. Read files
# -----------------------------------

jd_text = read_text_file(
    JD_PATH
)

resume_text = read_text_file(
    RESUME_PATH
)


# -----------------------------------
# 3. Calculate score
# -----------------------------------

result = calculate_final_score(
    jd_text,
    resume_text
)


# -----------------------------------
# 4. Display result
# -----------------------------------

print("\n")
print("=" * 60)
print("       AI RESUME SCREENING RESULT")
print("=" * 60)

print(
    f"\nFinal Score       : "
    f"{result['final_score']}%"
)

print(
    f"NLP Similarity    : "
    f"{result['similarity_score']}%"
)

print(
    f"Skill Match       : "
    f"{result['skill_score']}%"
)

print(
    f"Experience Match  : "
    f"{result['experience_score']}%"
)

print(
    f"Education Match   : "
    f"{result['education_score']}%"
)

print(
    f"\nRequired Experience : "
    f"{result['required_experience']} years"
)

print(
    f"Candidate Experience: "
    f"{result['candidate_experience']} years"
)

print("\nMatched Skills:")

for skill in result["matched_skills"]:

    print(f"  ✓ {skill}")


print("\nMissing Skills:")

for skill in result["missing_skills"]:

    print(f"  ✗ {skill}")


print(
    f"\nRecommendation: "
    f"{result['recommendation']}"
)

print("=" * 60) 