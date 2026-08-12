from pathlib import Path

import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(
    exist_ok=True
)


def prepare_dataframe(results):

    rows = []

    for result in results:

        rows.append({

            "Rank":
                result.get("rank", ""),

            "Candidate":
                result.get(
                    "candidate_name",
                    ""
                ),

            "Resume":
                result.get(
                    "filename",
                    ""
                ),

            "Final Score":
                result.get(
                    "final_score",
                    0
                ),

            "NLP Similarity":
                result.get(
                    "similarity_score",
                    0
                ),

            "Skill Match":
                result.get(
                    "skill_score",
                    0
                ),

            "Experience Match":
                result.get(
                    "experience_score",
                    0
                ),

            "Education Match":
                result.get(
                    "education_score",
                    0
                ),

            "Recommendation":
                result.get(
                    "recommendation",
                    ""
                ),

            "Matched Skills":
                ", ".join(
                    result.get(
                        "matched_skills",
                        []
                    )
                ),

            "Missing Skills":
                ", ".join(
                    result.get(
                        "missing_skills",
                        []
                    )
                ),

            "Status":
                result.get(
                    "status",
                    ""
                )
        })

    return pd.DataFrame(rows)


def generate_csv(results):

    dataframe = prepare_dataframe(
        results
    )

    output_path = (
        OUTPUT_DIR
        / "resume_screening_report.csv"
    )

    dataframe.to_csv(
        output_path,
        index=False
    )

    return output_path


def generate_excel(results):

    dataframe = prepare_dataframe(
        results
    )

    output_path = (
        OUTPUT_DIR
        / "resume_screening_report.xlsx"
    )

    dataframe.to_excel(
        output_path,
        index=False
    )

    return output_path


def generate_pdf(results):

    output_path = (
        OUTPUT_DIR
        / "resume_screening_report.pdf"
    )

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(
        "AI Resume Screening Report",
        styles["Title"]
    )

    story.append(title)

    story.append(
        Spacer(1, 20)
    )

    table_data = [[
        "Rank",
        "Candidate",
        "Score",
        "Skills",
        "Recommendation"
    ]]

    for result in results:

        table_data.append([

            str(
                result.get(
                    "rank",
                    ""
                )
            ),

            str(
                result.get(
                    "candidate_name",
                    ""
                )
            ),

            f"{result.get('final_score', 0)}%",

            f"{result.get('skill_score', 0)}%",

            str(
                result.get(
                    "recommendation",
                    ""
                )
            )
        ])

    table = Table(
        table_data,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            )

        ])
    )

    story.append(table)

    story.append(
        Spacer(1, 20)
    )

    # Detailed section
    for result in results:

        story.append(
            Paragraph(
                f"<b>#{result.get('rank')} "
                f"{result.get('candidate_name')}</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                f"Final Score: "
                f"{result.get('final_score')}%",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Recommendation: "
                f"{result.get('recommendation')}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                "Matched Skills: "
                + ", ".join(
                    result.get(
                        "matched_skills",
                        []
                    )
                ),
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                "Missing Skills: "
                + ", ".join(
                    result.get(
                        "missing_skills",
                        []
                    )
                ),
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1, 12)
        )

    document.build(story)

    return output_path