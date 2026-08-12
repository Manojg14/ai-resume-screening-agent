from pathlib import Path
import uuid

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)

from services.parser import (
    extract_text,
    allowed_file
)

from services.scoring import (
    calculate_final_score
)

from services.batch_analyzer import (
    analyze_multiple_resumes
)

from services.report_generator import (
    generate_csv,
    generate_excel,
    generate_pdf
)


# ==================================================
# Flask Application
# ==================================================

app = Flask(__name__)

app.secret_key = "change-this-secret-key"


# ==================================================
# Directories
# ==================================================

BASE_DIR = Path(
    __file__
).resolve().parent

UPLOAD_FOLDER = (
    BASE_DIR / "uploads"
)

UPLOAD_FOLDER.mkdir(
    exist_ok=True
)


OUTPUT_FOLDER = (
    BASE_DIR / "outputs"
)

OUTPUT_FOLDER.mkdir(
    exist_ok=True
)


# ==================================================
# Configuration
# ==================================================

app.config[
    "UPLOAD_FOLDER"
] = str(UPLOAD_FOLDER)

app.config[
    "MAX_CONTENT_LENGTH"
] = 50 * 1024 * 1024


# ==================================================
# Home
# ==================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ==================================================
# Single Resume Analysis
# ==================================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()

    resume = request.files.get(
        "resume"
    )

    if not job_description:

        flash(
            "Please enter a Job Description."
        )

        return redirect(
            url_for("index")
        )

    if not resume:

        flash(
            "Please upload a resume."
        )

        return redirect(
            url_for("index")
        )

    if resume.filename == "":

        flash(
            "Please select a resume."
        )

        return redirect(
            url_for("index")
        )

    if not allowed_file(
        resume.filename
    ):

        flash(
            "Only PDF, DOCX and TXT files are supported."
        )

        return redirect(
            url_for("index")
        )

    extension = Path(
        resume.filename
    ).suffix.lower()

    unique_filename = (
        f"{uuid.uuid4().hex}"
        f"{extension}"
    )

    file_path = (
        UPLOAD_FOLDER
        / unique_filename
    )

    resume.save(
        str(file_path)
    )

    try:

        resume_text = extract_text(
            file_path
        )

        result = calculate_final_score(
            job_description,
            resume_text
        )

        candidate_name = Path(
            resume.filename
        ).stem

        return render_template(
            "result.html",
            result=result,
            candidate_name=candidate_name,
            filename=resume.filename
        )

    except Exception as error:

        flash(
            f"Analysis failed: {error}"
        )

        return redirect(
            url_for("index")
        )


# ==================================================
# Multiple Resume Analysis
# ==================================================

@app.route(
    "/batch-analyze",
    methods=["POST"]
)
def batch_analyze():

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()

    resumes = request.files.getlist(
        "resumes"
    )

    if not job_description:

        flash(
            "Please enter a Job Description."
        )

        return redirect(
            url_for("index")
        )

    if not resumes:

        flash(
            "Please upload resumes."
        )

        return redirect(
            url_for("index")
        )

    saved_files = []

    original_names = []

    for resume in resumes:

        if not resume.filename:
            continue

        if not allowed_file(
            resume.filename
        ):

            continue

        extension = Path(
            resume.filename
        ).suffix.lower()

        unique_filename = (
            f"{uuid.uuid4().hex}"
            f"{extension}"
        )

        file_path = (
            UPLOAD_FOLDER
            / unique_filename
        )

        resume.save(
            str(file_path)
        )

        saved_files.append(
            file_path
        )

        original_names.append(
            resume.filename
        )

    if not saved_files:

        flash(
            "No valid resumes were uploaded."
        )

        return redirect(
            url_for("index")
        )

    try:

        results = []

        for file_path, original_name in zip(
            saved_files,
            original_names
        ):

            try:

                resume_text = extract_text(
                    file_path
                )

                result = calculate_final_score(
                    job_description,
                    resume_text
                )

                result["filename"] = (
                    original_name
                )

                result["candidate_name"] = (
                    Path(
                        original_name
                    ).stem
                )

                result["status"] = (
                    "Success"
                )

                results.append(result)

            except Exception as error:

                results.append({

                    "filename":
                        original_name,

                    "candidate_name":
                        Path(
                            original_name
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

                    "recommendation":
                        "Analysis Failed",

                    "status":
                        f"Failed: {error}"
                })

        # Sort
        results.sort(
            key=lambda x: x.get(
                "final_score",
                0
            ),
            reverse=True
        )

        # Ranking
        for rank, result in enumerate(
            results,
            start=1
        ):

            result["rank"] = rank

        # Store results in session-like
        # simple application memory
        app.config[
            "LAST_RESULTS"
        ] = results

        app.config[
            "LAST_JD"
        ] = job_description

        return render_template(
            "batch_result.html",
            results=results
        )

    except Exception as error:

        flash(
            f"Batch analysis failed: {error}"
        )

        return redirect(
            url_for("index")
        )


# ==================================================
# Candidate Details
# ==================================================

@app.route(
    "/candidate/<int:rank>"
)
def candidate(rank):

    results = app.config.get(
        "LAST_RESULTS",
        []
    )

    candidate_result = None

    for result in results:

        if result.get(
            "rank"
        ) == rank:

            candidate_result = result

            break

    if candidate_result is None:

        flash(
            "Candidate not found."
        )

        return redirect(
            url_for("index")
        )

    return render_template(
        "candidate.html",
        result=candidate_result
    )


# ==================================================
# CSV Report
# ==================================================

@app.route(
    "/download/csv"
)
def download_csv():

    results = app.config.get(
        "LAST_RESULTS",
        []
    )

    if not results:

        flash(
            "No analysis results available."
        )

        return redirect(
            url_for("index")
        )

    output = generate_csv(
        results
    )

    return send_file(
        output,
        as_attachment=True,
        download_name="resume_screening_report.csv"
    )


# ==================================================
# Excel Report
# ==================================================

@app.route(
    "/download/excel"
)
def download_excel():

    results = app.config.get(
        "LAST_RESULTS",
        []
    )

    if not results:

        flash(
            "No analysis results available."
        )

        return redirect(
            url_for("index")
        )

    output = generate_excel(
        results
    )

    return send_file(
        output,
        as_attachment=True,
        download_name="resume_screening_report.xlsx"
    )


# ==================================================
# PDF Report
# ==================================================

@app.route(
    "/download/pdf"
)
def download_pdf():

    results = app.config.get(
        "LAST_RESULTS",
        []
    )

    if not results:

        flash(
            "No analysis results available."
        )

        return redirect(
            url_for("index")
        )

    output = generate_pdf(
        results
    )

    return send_file(
        output,
        as_attachment=True,
        download_name="resume_screening_report.pdf"
    )


# ==================================================
# Run
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True
    ) 