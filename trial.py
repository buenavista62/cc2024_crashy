#!/usr/bin/env python3

"""Program to play with image LLMs."""

import base64
import logging
from pathlib import Path

import kagglehub
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()


class AccidentReport(BaseModel):
    """An accident report model."""

    damage_recognized: bool
    detailed_damage_description: str
    car_plate_numbers: list[str]


prompt = """You are a helpful car crash assistant called crashy.
Assemble a detailed report with the given output format.
Use all provided images and ask for additional images if required.
Only describe damage specific details of the pictures.
"""


def get_dataset() -> list[Path]:
    """Assert kaggle image data is cached."""
    path = kagglehub.dataset_download("humansintheloop/car-parts-and-car-damages")
    base = Path(path) / "Car damages dataset" / "File1" / "img"
    return [
        base / "Car damages 158.png",
        base / "Car damages 1492.png",
        base / "Car damages 1335.png",
        base / "Car damages 250.png",
    ]


def encode_image(image_path: Path) -> str:
    """Encode the given image."""
    with image_path.open("rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


for image_path in get_dataset():
    # Getting the base64 string
    base64_image = encode_image(image_path)

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ],
        response_format=AccidentReport,
        temperature=0.2,
    )

    logging.info(response.choices[0])
