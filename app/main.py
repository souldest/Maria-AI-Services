from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.routers.forecast_agent import router as forecast_router
from app.database import get_db

app = FastAPI(title="Maria AI – Umsatz & Vorrat Forecast API")

# Forecast-Router einbinden
app.include_router(forecast_router, prefix="/forecast", tags=["Forecast"])

# Root-Endpoint
@app.get("/")
def root():
    return {"message": "Maria AI Forecast API läuft!"}

# Optional: DB-Test-Endpoint
@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    result = db.execute("SELECT 1").scalar()
    return {"db_result": result}
