from celery import shared_task
from PIL import Image
from pathlib import Path


@shared_task
def convert_to_webp(source: Path):
    destination = source.with_suffix(".webp")

    image = Image.open(source)
    image.save(destination, format="webp")

    return destination
