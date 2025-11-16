# streamlit_app.py (Frontend)
import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Backend-Pfad hinzufügen, damit Imports funktionieren
sys.path.append(os.path.abspath("../backend"))

# Backend-Module importieren
from data_loader import load_data
from app.routers.forecast_agent import EnterpriseForecastAgent

st.title("Forecast Agent: Umsatz & Vorrat Vorhersage")

uploaded_file = st.file_uploader("CSV Datei hochladen", type=["csv"])
if uploaded_file:
    df = load_data(uploaded_file)
    st.write("Daten Vorschau:")
    st.dataframe(df.head())

    agent = EnterpriseForecastAgent()

    # Umsatz Vorhersage
    st.header("Umsatz Prognose")
    sales_forecast = agent.forecast_sales(df)
    st.dataframe(sales_forecast)

    # Vorrat Vorhersage
    st.header("Vorrat Prognose")
    inventory_forecast = agent.forecast_inventory(df)
    st.dataframe(inventory_forecast)
