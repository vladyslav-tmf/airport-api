import uuid
from pathlib import Path

from django.utils.text import slugify

from models import Airplane


def airplane_image_file_path(instance: "Airplane", filename: str) -> Path:
    """
    Generate unique file path for airplane image uploads.

    Creates a unique filename by combining the slugfield airplane name with a UUID.
    Places the file in the "uploads/airplanes/" directory.
    """
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}" + Path(filename).suffix
    return Path("uploads/airplanes/") / Path(filename)
