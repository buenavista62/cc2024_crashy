"""Module to manage LLM calls."""

import io

from openai import OpenAI
from openai.types.chat.parsed_chat_completion import ContentType

from model import DamageReport
from prompt import prompt

client = OpenAI()


def call_transcription(audio_file: io.BytesIO) -> str:
    """Call the transcription API with the audio file."""
    translation = client.audio.translations.create(
        model="whisper-1",
        file=audio_file,
    )
    return translation.text


def call_llm(
    audio_transcript: str | None, base64_images: list[str]
) -> ContentType | None:
    """Call the LLM  with the list of images."""
    if not audio_transcript:
        user_input = []
    else:
        user_input = [{"type": "text", "text": "<Record>: " + audio_transcript}]
    for base64_image in base64_images:
        content = {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
        }
        user_input.append(content)

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
                "content": user_input,
            },
        ],
        response_format=DamageReport,
        temperature=0.1,
    )
    return response.choices[0].message.parsed
