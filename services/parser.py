from pathlib import Path


def read_text_file(file_path):

    "Read the Text File"

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    ) 

from pathlib import Path

import fitz
from docx import Document


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


def allowed_file(filename):

    extension = Path(filename).suffix.lower()

    return extension in ALLOWED_EXTENSIONS


def extract_pdf_text(file_path):

    text = []

    with fitz.open(file_path) as pdf:

        for page in pdf:

            page_text = page.get_text()

            if page_text:

                text.append(page_text)

    return "\n".join(text)


def extract_docx_text(file_path):

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            paragraphs.append(
                paragraph.text
            )

    return "\n".join(paragraphs)


def extract_txt_text(file_path):

    return Path(file_path).read_text(
        encoding="utf-8",
        errors="ignore"
    )


def extract_text(file_path):

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension == ".pdf":

        return extract_pdf_text(
            file_path
        )

    elif extension == ".docx":

        return extract_docx_text(
            file_path
        )

    elif extension == ".txt":

        return extract_txt_text(
            file_path
        )

    else:

        raise ValueError(
            f"Unsupported file format: {extension}"
        ) 