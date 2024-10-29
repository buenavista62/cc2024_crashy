"""Program to play with image LLMs."""

import base64

import streamlit as st
from openai import OpenAI

from llm import call_llm
from model import DamageReport

client = OpenAI()
st.title("Crashy App")


def check_damage_report(final_resp: DamageReport) -> dict[str, bool]:
    """Check all conditions and return a dictionary of problems."""
    return {
        "car_not_visible": not all(final_resp.car_present),
        "no_damage": not final_resp.damage_recognized,
        "multiple_vehicles": final_resp.number_of_unique_vehicles > 1,
        "damage_not_visible": not final_resp.damage_fully_visible,
        "fire_present": final_resp.is_fire_present,
    }


uploaded_file = st.file_uploader(
    "Bitte laden Sie ein " "Bild vom Schaden hoch",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
)


if uploaded_file:
    with st.spinner("Analysiere Bilder..."):
        n_cols = (len(uploaded_file) + 3) // 4
        cols = st.columns(n_cols)
        for i in range(len(uploaded_file)):
            cols[i % n_cols].image(
                uploaded_file[i], caption=f"Foto Nr. {i+1}", use_column_width=True
            )

        # Function to encode the image
        def encode_image(data: list[bytes]) -> list[str]:
            """Encode the given image."""
            return [base64.b64encode(img).decode("utf-8") for img in data]

        base64_images = encode_image([file.getvalue() for file in uploaded_file])
        img_content = []
        for base64_image in base64_images:
            content = {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            }
            img_content.append(content)

        final_resp = call_llm(base64_images)

    st.write(final_resp)
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
            enumerate(final_resp.car_present) if not visible])}",
            "no_damage": "Kein Schaden erkannt. Bitte laden Sie ein"
            "Bild mit sichtbarem Schaden hoch.",
            "multiple_vehicles": "Mehrere Fahrzeuge auf dem Bild."
            "Bitte laden Sie Bilder nur von einem Fahrzeug hoch.",
            "damage_not_visible": "Schaden nicht vollständig sichtbar."
            "Bitte laden Sie ein Bild mit vollständig sichtbarem Schaden hoch.",
        }

        # Check if any problems exist
        active_problems = [
            msg for problem, msg in error_messages.items() if problems[problem]
        ]

        if active_problems:
            for message in active_problems:
                st.error(message)
            st.stop()

        if final_resp.is_fire_present:
            st.warning("Brandgefahr! Bitte entfernen Sie sich vom Fahrzeug.")

        st.write("Schadensbericht:")

        @st.fragment
        def fill_out_form() -> None:
            """Fill out the damage report form."""
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Name", placeholder="Ihr Name")
                st.text_input("Telefonnummer", placeholder="Ihre Telefonnummer")
                st.text_input("E-Mail-Adresse", placeholder="Ihre E-Mail-Adresse")
                st.text_area("Anschrift", placeholder="Ihre Anschrift")
            with col2:
                st.text_input("Kennzeichen", final_resp.license_plate_number)
                for damage in final_resp.detailed_damage_description:
                    st.checkbox(damage, value=True)


            st.write("Bitte überprüfen Sie die Angaben.")
            if st.button("Schaden melden"):
                ...

        fill_out_form()
