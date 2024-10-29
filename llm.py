"""Module to manage LLM calls."""

from openai import OpenAI
from openai.types.chat.parsed_chat_completion import ContentType

from model import DamageReport
from prompt import prompt

client = OpenAI()


def call_llm(base64_images: list[str]) -> ContentType | None:
    """Call the LLM  with the list of images."""
    img_content = []
    for base64_image in base64_images:
        content = {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
        }
        img_content.append(content)

    response = client.beta.chat.completions.parse(
        model="gpt-4o",
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
                "content": img_content,
            },
        ],
        response_format=DamageReport,
        temperature=0.1,
    )
    return response.choices[0].message.parsed
