"""Program to play with image LLMs."""

import base64
import datetime
import io

import streamlit as st
from openai import OpenAI
from streamlit.runtime.uploaded_file_manager import UploadedFile

from exif import ExifData
from llm import call_llm, call_transcription
from model import DamageReport

client = OpenAI()
st.title("Crashy")

st.write("## Dein digitaler Schadenmelder")
st.write(
    "Bitte erzähle uns vom Vorfall und lade Bilder hoch, um den Schaden zu melden."
)


def check_damage_report(final_resp: DamageReport) -> dict[str, bool]:
    """Check all conditions and return a dictionary of problems."""
    return {
        "car_not_visible": not all(final_resp.vehicle_present),
        "no_damage": not final_resp.damage_recognized,
        "multiple_vehicles": final_resp.number_of_unique_vehicles > 1,
        "fire_present": final_resp.is_fire_present,
        "collision_with_animal": final_resp.collision_with_animal,
        "is_theft": final_resp.is_theft,
    }


@st.cache_data(show_spinner="Aufzeichnung wird verarbeitet...")
def audio_input(audio_value: UploadedFile | None) -> str | None:
    """Capture audio input and return its transcription."""
    if audio_value:
        audio_bytes = audio_value.read()
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"
        return call_transcription(audio_file)

    return None


col_toggle, _ = st.columns(2)

with col_toggle:
    self_speak = st.toggle("Selber sprechen", value=True)
col_audio, col_image = st.columns(2)


with col_audio:
    if self_speak:
        audio_value = st.experimental_audio_input("Was ist passiert?")
    else:
        audio_value = st.file_uploader("Audio hochladen", type=["wav", "mp3"])
    if audio_value:
        transcription = audio_input(audio_value)
    try:
        if transcription:
            st.write(transcription)
    except NameError:
        pass

with col_image:
    uploaded_file = st.file_uploader(
        "Bilder hochladen",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )

if uploaded_file:
    n_cols = min(4, len(uploaded_file))
    cols = st.columns(n_cols)
    for i in range(len(uploaded_file)):
        cols[i % n_cols].image(
            uploaded_file[i], caption=f"Foto Nr. {i+1}", use_column_width=True
        )
    start_button = st.button("Analyse starten")


if "start_button" in locals() and start_button:
    if "damages" in st.session_state:
        del st.session_state["damages"]
    with st.spinner("Analysiere Bilder..."):

        def encode_image(data: list[bytes]) -> list[str]:
            """Encode the given image."""
            return [base64.b64encode(img).decode("utf-8") for img in data]

        images = [file.getvalue() for file in uploaded_file]
        base64_images = encode_image(images)
        img_content = []
        for base64_image in base64_images:
            content = {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            }
            img_content.append(content)

        try:
            audio_str = transcription
        except NameError:
            audio_str = None

        final_resp = call_llm(audio_str, base64_images)

        exif = ExifData(images)

        if exif.creation_times:
            try:
                first_valid_time = next(time for time in exif.creation_times if time)
                dt = datetime.datetime.strptime(
                    first_valid_time, "%Y:%m:%d %H:%M:%S"
                ).replace(tzinfo=datetime.timezone.utc)
            except StopIteration:
                dt = None

        map_data = (
            {
                "latitude": [ex[0] for ex in exif.locations if ex],
                "longitude": [ex[1] for ex in exif.locations if ex],
            }
            if exif.locations
            else None
        )

    st.json(final_resp, expanded=False)
    if not final_resp:
        st.write(
            "Das Bild konnte leider nicht analysiert werden. "
            "Bitte laden Sie ein neues Bild hoch"
        )
    if final_resp:
        problems = check_damage_report(final_resp)

        error_messages = {
            "car_not_visible": "Auf mindestens einem Bild ist das Auto nicht sichtbar. "
            "Bitte laden Sie ein Bild vom gesamten Fahrzeug hoch. Betroffene Bilder:"
            f"{', '.join([f'Bild Nr {i+1!s}' for i, visible in
            enumerate(final_resp.vehicle_present) if not visible])}",
            "no_damage": "Es wurde kein Schaden erkannt. Bitte laden Sie ein "
            "Bild mit sichtbarem Schaden hoch.",
            "multiple_vehicles": "Mehrere Fahrzeuge auf dem Bild. "
            "Bitte laden Sie Bilder nur von einem Fahrzeug hoch.",
            "fire_present": "Brandgefahr erkannt. Bitte entfernen Sie sich "
            "vom Fahrzeug.",
            "collision_with_animal": "Kollision mit einem Tier erkannt. ",
            "is_theft": "Diebstahl erkannt.",
        }

        # Check if any problems exist
        active_problems = [
            msg for problem, msg in error_messages.items() if problems[problem]
        ]

        if active_problems:
            for message in active_problems:
                st.warning(message)

        if final_resp.is_fire_present:
            st.warning("Brandgefahr! Bitte entfernen Sie sich vom Fahrzeug.")

        st.write("Schadensbericht:")

        @st.fragment
        def fill_out_form() -> None:
            """Fill out the damage report form."""
            if "damages" not in st.session_state:
                st.session_state.damages = final_resp.detailed_damage_description.copy()
            col1, col2 = st.columns(2)
            with col1:
                try:
                    if transcription:
                        st.text_area(label="Das ist passiert:", value=transcription)
                except NameError:
                    st.text_area(label="Das ist passiert:", value="")

                st.text_input("Kennzeichen", final_resp.license_plate_number)
                estimated_repair_cost = final_resp.estimated_repair_cost * 2.5
                st.write(f"Kostenschätzung: {estimated_repair_cost:.2f} CHF")

                st.write("### Aktuelle Schäden")
                for idx, damage in enumerate(st.session_state.damages):
                    st.checkbox(damage, value=True, key=f"damage_{idx}")

                new_damage = st.text_input("Fügen Sie zusätzliche Schäden hinzu")

                try:
                    if new_damage and new_damage not in st.session_state.damages:
                        st.session_state.damages.append(new_damage)
                        st.toast(f"Schaden '{new_damage}' hinzugefügt.")
                        new_damage = ""
                        st.rerun(scope="fragment")

                except ValueError as e:
                    st.exception(e)
                    st.error("Schaden konnte nicht hinzugefügt werden.")
            with col2:
                if dt:
                    st.date_input("Datum", dt.date())
                    st.time_input("Uhrzeit", dt.time())
                if map_data:
                    st.map(map_data)

            st.write("Bitte überprüfen Sie die Angaben.")
            if st.button("Schaden melden"):
                ...

        fill_out_form()
