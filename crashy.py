"""Program to play with image LLMs."""

import base64
from typing import Optional

import streamlit as st
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()
st.title("Crashy App")


class AccidentReport(BaseModel):
    """An accident report model."""

    car_present: bool
    damage_recognized: bool
    damage_fully_visible: bool
    damage_severity: str  # 'low', 'medium', 'high'
    damage_location: str  # z.B. 'Front', 'Heck', 'Seiten', 'Dach'
    fire_present: bool
    license_plate_number: Optional[str]  # noqa: UP007
    detailed_damage_description: str
    number_of_valid_images: int
    number_of_unique_vehicles: int


prompt = """
    Sie sind ein hilfreicher Assistent für Autounfälle namens "crashy". Ihre Aufgabe
    ist es,
    einen umfassenden Schadensbericht basierend auf den bereitgestellten Fahrzeugbildern
    auf Deutsch zu
    erstellen. Nutzen Sie alle bereitgestellten Bilder und fordern Sie bei Bedarf
    zusätzliche
    Bilder oder Details an, um eine genaue Bewertung vornehmen zu können. Beschreiben
    Sie
    ausschließlich die sichtbaren Schäden auf den Bildern und vermeiden Sie es,
    zusätzliche
    Informationen einzubeziehen.

    Folgende Angaben müssen im Bericht enthalten sein:

    1. **Fahrzeug vorhanden**:
    - Bestätigen Sie, dass das Fahrzeug auf den Bildern vollständig sichtbar ist.
    - **Erforderlich**: Ja

    2. **Erkannter Schaden**:
    - Bestätigen Sie, dass Schäden am Fahrzeug erkennbar sind.
    - **Erforderlich**: Ja

    3. **Vollständige Sichtbarkeit des Schadens**:
    - Bestätigen Sie, dass der Schaden vollständig auf den Bildern sichtbar ist.
    - **Erforderlich**: Ja

    4. **Schweregrad des Schadens**:
    - Bewerten Sie den Schaden als niedrig, mittel oder hoch.
    - **Erforderlich**: Nein

    5. **Schadensort am Fahrzeug**:
    - Geben Sie an, wo sich der Schaden am Fahrzeug befindet (z.B. Front, Heck, Seiten,
    Dach).
    - **Erforderlich**: Nein

    6. **Brandgefahr**:
    - Bestätigen Sie, ob Anzeichen von Brand vorhanden sind (Ja/Nein).
    - **Erforderlich**: Nein

    7. **Kennzeichen**:
    - Erfassen Sie das Kennzeichen nur, wenn es klar lesbar und vollständig
    erkennbar ist und jedes Zeichen zu 100% sichtbar ist.
    - Wenn das Kennzeichen nicht zu 100% sichtbar ist, geben Sie `None` an.
    - **Erforderlich**: Nein

    8. **Zusätzliche Details**:
    - Fügen Sie eine detaillierte Beschreibung der sichtbaren Schäden hinzu,
        einschließlich
    der betroffenen Fahrzeugteile und der Art des Schadens
    (z.B. Dellen, Kratzer, gebrochene Spiegel).

    9. **Anzahl der gültigen Bilder**:
    - Geben Sie die Anzahl der Bilder an, die für die Bewertung des Schadens
    verwendet wurden. Ungültige Bilder sollten nicht berücksichtigt werden.
    - **Erforderlich**: Ja

    10. **Anzahl der eindeutigen Fahrzeuge**:
    - Geben Sie die Anzahl der eindeutigen Fahrzeuge an, die auf den Bildern
    zu sehen sind. Wenn mehrere Fahrzeuge auf den Bildern sichtbar sind, geben
    Sie die Anzahl der unterschiedlichen Fahrzeuge an.

    **Beispiel**:
    - Fahrzeug vorhanden: Ja
    - Erkannter Schaden: Ja
    - Vollständige Sichtbarkeit des Schadens: Ja
    - Schweregrad des Schadens: Mittel
    - Schadensort am Fahrzeug: Front
    - Brandgefahr: Nein
    - Kennzeichen: None
    - Zusätzliche Details: Es gibt eine große Delle auf der Motorhaube und
    einen Kratzer auf der Stoßstange.
    - Anzahl der gültigen Bilder: 3
    - Anzahl der eindeutigen Fahrzeuge: 1


    """


uploaded_file = st.file_uploader(
    "Bitte laden Sie ein " "Bild vom Schaden hoch",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
)


if uploaded_file:
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
        response_format=AccidentReport,
        temperature=0.1,
    )

    st.write(response.choices[0].message.parsed)
    final_resp = response.choices[0].message.parsed
    if not final_resp:
        st.write(
            "Das Bild konnte leider nicht analysiert werden. "
            "Bitte laden Sie ein Bild vom gesamten Fahrzeug hoch."
        )
    else:
        if not final_resp.car_present:
            st.write(
                "Das Auto ist nicht sichtbar. "
                "Bitte laden Sie ein Bild vom gesamten Fahrzeug hoch."
            )
            st.stop()
        if not final_resp.damage_recognized:
            st.write(
                "Kein Schaden erkannt. "
                "Bitte laden Sie ein Bild mit sichtbarem Schaden hoch."
            )
            st.stop()
        if not final_resp.damage_fully_visible:
            st.write(
                "Schaden nicht vollständig sichtbar. "
                "Bitte laden Sie ein Bild mit vollständig sichtbarem Schaden hoch."
            )
            st.stop()
        if final_resp.fire_present:
            st.warning("Brandgefahr!")
            st.stop()
        if final_resp.damage_severity == "high":
            st.warning("Hoher Schaden!")
            st.stop()

        st.write("Schadensbericht:")

        @st.fragment
        def fill_out_form() -> None:

            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Name", placeholder="Ihr Name")
                st.text_input("Telefonnummer", placeholder="Ihre Telefonnummer")
                st.text_input("E-Mail-Adresse", placeholder="Ihre E-Mail-Adresse")
                st.text_area("Anschrift", placeholder="Ihre Anschrift")
            with col2:
                st.text_input("Schweregrad des Schadens", final_resp.damage_severity)
                st.text_input("Schadensort am Fahrzeug", final_resp.damage_location)
                st.text_input("Kennzeichen", final_resp.license_plate_number)
                st.text_area(
                    "Zusätzliche Details", final_resp.detailed_damage_description
                )
            st.write("Bitte überprüfen Sie die Angaben.")
            if st.button("Schaden melden"):
                ...
        fill_out_form()
