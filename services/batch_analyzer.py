from pathlib import Path

from .parser import extract_text, allowed_file
from .scoring import calculate_final_score


def analyze_resume_file(
    file_path,
    job_description,
    original_filename=None
):
    """
    Analyze one resume against a Job Description.
    """

    file_path = Path(file_path)

    resume_text = extract_text(file_path)

    if not resume_text.strip():
        raise ValueError(
            "Could not extract text from resume."
        )

    result = calculate_final_score(
        job_description,
        resume_text
    )

    filename = (
        original_filename
        if original_filename
        else file_path.name
    )

    result["filename"] = filename

    result["candidate_name"] = file_path.stem

    return result


def analyze_multiple_resumes(
    file_paths,
    job_description
):
    """
    Analyze multiple resumes and return
    candidates sorted by final score.
    """

    results = []

    for file_path in file_paths:

        try:

            result = analyze_resume_file(
                file_path,
                job_description
            )

            result["status"] = "Success"

            results.append(result)

        except Exception as error:

            results.append({

                "filename": Path(
                    file_path
                ).name,

                "candidate_name": Path(
                    file_path
                ).stem,

                "final_score": 0,

                "similarity_score": 0,

                "skill_score": 0,

                "experience_score": 0,

                "education_score": 0,

                "matched_skills": [],

                "missing_skills": [],

                "required_experience": 0,

                "candidate_experience": 0,

                "recommendation": "Analysis Failed",

                "status": f"Failed: {error}"

            })

    # Rank candidates
    results.sort(
        key=lambda x: x.get(
            "final_score",
            0
        ),
        reverse=True
    )

    # Add ranking
    for index, result in enumerate(
        results,
        start=1
    ):

        result["rank"] = index

    return results