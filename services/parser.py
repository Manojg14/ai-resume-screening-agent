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