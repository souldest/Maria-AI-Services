from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import forecast  # forecast.py mit Sales & Inventory Router

app = FastAPI(
    title="AI Sales & Inventory Forecast API",
    description="API zur Umsatz- und Lagerbestandsvorhersage mit Prophet, ML & Zeitreihenanalyse",
    version="1.0.0"
)

# Sichere CORS-Konfiguration
origins = [
    "http://localhost:8501",  # Für lokale Frontend-Entwicklung (Streamlit)
    "https://myfrontendapp-xyz.westeurope.azurecontainerapps.io"  # Ersetze durch deine Frontend-Domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router einbinden
app.include_router(forecast.router, prefix="/forecast", tags=["forecast"])

# Root-Endpunkt
@app.get("/")
def root():
    return {"message": "Willkommen beim AI Sales & Inventory Forecast API"}

# Optional: main für lokalen Start
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Damit es innerhalb von Docker erreichbar ist
        port=8000,
        reload=True      # Nur lokal, für Hot-Reload
    )
