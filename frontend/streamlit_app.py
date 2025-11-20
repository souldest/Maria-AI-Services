import streamlit as st
import requests

# ----------------------------------------
# Backend-URL (intern im Container)
# ----------------------------------------
BACKEND_URL = "http://localhost:8000/forecast"

# ----------------------------------------
# Streamlit App
# ----------------------------------------
st.title("Maria AI Forecast Dashboard")

# Auswahl der Forecast-Art
forecast_type = st.radio("Forecast Type", ["Sales", "Inventory"])

if st.button("Get Forecast"):
    if forecast_type == "Sales":
        url = f"{BACKEND_URL}/sales"
    else:
        url = f"{BACKEND_URL}/inventory"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        st.write(f"### {forecast_type} Forecast")
        st.json(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Fehler beim Abrufen der Daten: {e}")
