"""Program to play with image LLMs."""

import base64

import streamlit as st

from llm import call_llm

st.title("Crashy App")


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
    final_resp = call_llm(base64_images)

    st.write(final_resp)
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
                for damage in final_resp.detailed_damage_description:
                    st.checkbox(damage, value=True)
            st.write("Bitte überprüfen Sie die Angaben.")
            if st.button("Schaden melden"):
                ...

        fill_out_form()
