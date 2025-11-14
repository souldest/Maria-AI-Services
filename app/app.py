from routers.forecast_agent import ForecastAgent
from services.some_service import SomeService
import streamlit as st

st.title("Maria AI Forecast Dashboard")

# Forecast Agent initialisieren
agent = ForecastAgent()

# Umsatz forecast
st.header("Umsatz Prognose")
sales = agent.forecast_sales()
st.dataframe(sales)

# Vorrat forecast
st.header("Vorrat Prognose")
inventory = agent.forecast_inventory()
st.dataframe(inventory)
