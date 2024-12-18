import uuid
from pathlib import Path

from django.utils.text import slugify


def airplane_image_file_path(instance, filename):
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}" + Path(filename).suffix
    return Path("uploads/airplanes/") / Path(filename)
