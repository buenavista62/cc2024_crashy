#!/usr/bin/env python3

"""Program to evaluate the crashy prompt."""

import base64
import json
from pathlib import Path
from pprint import pformat
from typing import Any

import kagglehub

from llm import call_llm


def get_dataset() -> list[Path]:
    """Assert kaggle image data is cached."""
    path = kagglehub.dataset_download("humansintheloop/car-parts-and-car-damages")
    base = Path(path) / "Car damages dataset" / "File1" / "img"
    return [
        Path("images") / "hand.jpeg",
        Path("images") / "fire.jpg",
        base / "Car damages 319.png",
        base / "Car damages 158.png",
        base / "Car damages 1492.png",
        base / "Car damages 1335.png",
        base / "Car damages 250.png",
    ]


def encode_image(image_path: Path) -> str:
    """Encode the given image."""
    with image_path.open("rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


data: list[dict[str, Any]] = []
for image_path in get_dataset():
    # Getting the base64 string
    base64_image = encode_image(image_path)
    parsed = call_llm("", [base64_image])

    print(image_path)  # noqa: T201
    if parsed:
        print(pformat(parsed.model_dump()))  # noqa: T201
        data.append(parsed.model_dump())
with Path("data.json").open("w") as fp:
    fp.write(json.dumps(data, sort_keys=True, indent=2))
