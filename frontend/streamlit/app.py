import streamlit as st
import requests

st.title("Agenten Dashboard")

input_text = st.text_area("Eingabetext")

if st.button("Workflow starten"):
    response = requests.post(
        "http://localhost:8000/run",
        json={"text": input_text}
    )
    if response.ok:
        st.success("Workflow abgeschlossen!")
        st.write(response.json()["result"])
    else:
        st.error("Fehler beim Ausführen des Workflows")
