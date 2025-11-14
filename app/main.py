from fastapi import FastAPI
from routers import forecast_agent

app = FastAPI(title="Vorrat & Umsatz Forecast API")

app.include_router(forecast_agent.router, prefix="/forecast", tags=["Forecast"])
