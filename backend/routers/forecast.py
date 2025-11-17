from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Sale, Inventory
from prophet import Prophet
import pandas as pd

router = APIRouter(prefix="/forecast", tags=["forecast"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/sales")
def forecast_sales(db: Session = Depends(get_db)):
    # Daten abrufen
    sales_data = db.query(Sale.date, Sale.quantity).all()
    df = pd.DataFrame(sales_data, columns=["ds", "y"])
    if df.empty:
        return {"error": "Keine Daten"}
    
    # Prophet Forecast
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(30).to_dict(orient="records")

@router.get("/inventory")
def forecast_inventory(db: Session = Depends(get_db)):
    inventory_data = db.query(Inventory.date, Inventory.stock_level).all()
    df = pd.DataFrame(inventory_data, columns=["ds", "y"])
    if df.empty:
        return {"error": "Keine Daten"}
    
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(30).to_dict(orient="records")
