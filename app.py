from pathlib import Path
import uuid

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from services.parser import (
    extract_text,
    allowed_file
)

from services.scoring import (
    calculate_final_score
)


# ==========================================
# Flask Application
# ==========================================

app = Flask(__name__)

app.secret_key = "change-this-secret-key"


# ==========================================
# Project Directories
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_FOLDER = BASE_DIR / "uploads"

UPLOAD_FOLDER.mkdir(
    exist_ok=True
)


# ==========================================
# Flask Configuration
# ==========================================

app.config["UPLOAD_FOLDER"] = str(
    UPLOAD_FOLDER
)

app.config["MAX_CONTENT_LENGTH"] = (
    10 * 1024 * 1024
)


# ==========================================
# Home Page
# ==========================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ==========================================
# Resume Analysis
# ==========================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    # --------------------------------------
    # Get Job Description
    # --------------------------------------

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()


    # --------------------------------------
    # Get Resume
    # --------------------------------------

    resume = request.files.get(
        "resume"
    )


    # --------------------------------------
    # Validate JD
    # --------------------------------------

    if not job_description:

        flash(
            "Please enter a Job Description."
        )

        return redirect(
            url_for("index")
        )


    # --------------------------------------
    # Validate Resume
    # --------------------------------------

    if not resume:

        flash(
            "Please upload a resume."
        )

        return redirect(
            url_for("index")
        )


    if resume.filename == "":

        flash(
            "Please select a resume file."
        )

        return redirect(
            url_for("index")
        )


    # --------------------------------------
    # Validate File Extension
    # --------------------------------------

    if not allowed_file(
        resume.filename
    ):

        flash(
            "Only PDF, DOCX and TXT files are supported."
        )

        return redirect(
            url_for("index")
        )


    # --------------------------------------
    # Generate Safe Filename
    # --------------------------------------

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


    # --------------------------------------
    # Save Resume
    # --------------------------------------

    resume.save(
        str(file_path)
    )


    try:

        # ----------------------------------
        # Extract Resume Text
        # ----------------------------------

        resume_text = extract_text(
            file_path
        )


        if not resume_text.strip():

            flash(
                "Could not extract text from the resume."
            )

            return redirect(
                url_for("index")
            )


        # ----------------------------------
        # Run Stage 1 NLP Engine
        # ----------------------------------

        result = calculate_final_score(
            job_description,
            resume_text
        )


        # ----------------------------------
        # Candidate Name
        # ----------------------------------

        candidate_name = Path(
            resume.filename
        ).stem


        # ----------------------------------
        # Result Page
        # ----------------------------------

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


# ==========================================
# Run Flask Application
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )