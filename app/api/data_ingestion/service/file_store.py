from pathlib import Path
from datetime import datetime
import re
from fastapi import UploadFile


def clean_filename(name: str) -> str:
    """
    Converts filename to a safe, readable format:
    - lowercase
    - spaces → underscores
    - removes special characters
    """
    name = name.lower()
    name = name.replace(" ", "_")
    name = re.sub(r"[^a-z0-9_\-]", "", name)
    return name


def get_timestamp() -> str:
    """
    Machine timestamp at upload time
    Format: YYYYMMDD_HHMMSS
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_uploaded_file(upload_dir: Path, file: UploadFile) -> Path:
    original = Path(file.filename)

    cleaned_name = clean_filename(original.stem)
    timestamp = get_timestamp()
    extension = original.suffix.lower()

    final_filename = f"{cleaned_name}__{timestamp}{extension}"
    file_path = upload_dir / final_filename

    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())

    return file_path
