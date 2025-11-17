import streamlit as st
import requests
import pandas as pd

API_URL = "http://backend:8000/forecast"  # Docker interner Host

st.title("AI Sales & Inventory Forecast")

option = st.selectbox("Forecast für:", ["sales", "inventory"])

if st.button("Forecast anzeigen"):
    response = requests.get(f"{API_URL}/{option}")
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        st.line_chart(df.set_index("ds")["yhat"])
    else:
        st.error("Fehler beim Abrufen der Daten")
