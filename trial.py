#!/usr/bin/env python3

import base64
from openai import OpenAI
import kagglehub
from pathlib import Path

client = OpenAI()

# assert kaggle image data is cached
def get_dataset() -> list[Path]:
  path = kagglehub.dataset_download("humansintheloop/car-parts-and-car-damages")
  base = Path(path) / "Car damages dataset" / "File1" / "img"
  return [
    base  / "Car damages 158.png"
  ]

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

for image_path in get_dataset():
  # Getting the base64 string
  base64_image = encode_image(image_path)

  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "What is in this image?",
          },
          {
            "type": "image_url",
            "image_url": {
              "url":  f"data:image/jpeg;base64,{base64_image}"
            },
          },
        ],
      }
    ],
  )

  print(response.choices[0])

