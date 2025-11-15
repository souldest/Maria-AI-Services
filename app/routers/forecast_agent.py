from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from prophet import Prophet
import pandas as pd
from datetime import datetime, timedelta
from joblib import Parallel, delayed
from app.database import SessionLocal, engine
from typing import Dict, List

router = APIRouter()

# Dependency für DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Forecast Agent Klasse ---
class EnterpriseForecastAgent:
    """
    Forecast Agent für Umsatz & Vorrat.
    - Prophet Zeitreihenprognose
    - Lagerhistorie berücksichtigt
    - Dynamische Sicherheitsbestände
    - Warnungen & Nachbestellvorschläge
    - Optimiert für große Datensätze mit Parallelisierung
    """
    def __init__(self, db: Session, forecast_days: int = 14, base_safety_stock: int = 5, alert_callback=None):
        self.db = db
        self.forecast_days = forecast_days
        self.base_safety_stock = base_safety_stock
        self.alert_callback = alert_callback

    # --- Daten laden ---
    def fetch_sales_data(self) -> pd.DataFrame:
        query = "SELECT router_id, amount, created_at FROM sales ORDER BY created_at ASC"
        return pd.read_sql(query, self.db.bind)

    def fetch_inventory_data(self) -> pd.DataFrame:
        query = "SELECT router_id, product_name, stock_level FROM inventory"
        return pd.read_sql(query, self.db.bind)

    # --- Prophet Forecast Helper ---
    def _forecast_timeseries(self, df: pd.DataFrame, value_col: str) -> pd.DataFrame:
        if df.empty or len(df) < 3:
            return pd.DataFrame({
                'ds': [datetime.now() + timedelta(days=i) for i in range(self.forecast_days)],
                'yhat': [df[value_col].mean() if not df.empty else 0] * self.forecast_days,
                'yhat_lower': [0] * self.forecast_days,
                'yhat_upper': [0] * self.forecast_days
            })
        ts = df.rename(columns={'created_at': 'ds', value_col: 'y'})
        model = Prophet(daily_seasonality=True, weekly_seasonality=True, yearly_seasonality=True)
        model.fit(ts)
        future = model.make_future_dataframe(periods=self.forecast_days)
        forecast = model.predict(future)
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(self.forecast_days)

    # --- Umsatz Forecast ---
    def forecast_sales(self) -> Dict[int, pd.DataFrame]:
        df = self.fetch_sales_data()
        def forecast_router(rid, group):
            return rid, self._forecast_timeseries(group.groupby('created_at')['amount'].sum().reset_index(), 'y')
        results = Parallel(n_jobs=-1)(delayed(forecast_router)(rid, group) for rid, group in df.groupby('router_id'))
        return dict(results)

    # --- Vorrat Forecast ---
    def forecast_inventory(self) -> Dict[int, List[Dict]]:
        inventory_df = self.fetch_inventory_data()
        sales_forecasts = self.forecast_sales()
        restock_suggestions = {}

        for rid, products in inventory_df.groupby('router_id'):
            forecast = sales_forecasts.get(rid)
            total_expected_sales = forecast['yhat'].sum() if forecast is not None else 0
            safety_stock = self.base_safety_stock + int(forecast['yhat_upper'].std() if forecast is not None else 0)

            suggestions = []
            for _, product in products.iterrows():
                reorder_qty = max(0, int(total_expected_sales - product['stock_level'] + safety_stock))
                status = "LOW" if product['stock_level'] < safety_stock else "OK"

                if status == "LOW" and self.alert_callback:
                    self.alert_callback(rid, product['product_name'], product['stock_level'], reorder_qty)

                suggestions.append({
                    "product_name": product['product_name'],
                    "current_stock": product['stock_level'],
                    "expected_sales": round(total_expected_sales, 2),
                    "safety_stock": safety_stock,
                    "reorder_quantity": reorder_qty,
                    "status": status
                })
            restock_suggestions[rid] = suggestions

        return restock_suggestions

# --- Beispiel Alert Callback ---
def slack_alert(router_id, product_name, current_stock, reorder_qty):
    print(f"[ALERT] Router {router_id}, Produkt {product_name} niedrig: {current_stock} Stück, Nachbestellung: {reorder_qty}")

# --- FastAPI Endpoints ---
@router.get("/sales")
def predict_sales(db: Session = Depends(get_db)):
    agent = EnterpriseForecastAgent(db)
    return agent.forecast_sales()

@router.get("/inventory")
def predict_inventory(db: Session = Depends(get_db)):
    agent = EnterpriseForecastAgent(db, alert_callback=slack_alert)
    return agent.forecast_inventory()

@router.get("/inventory-report")
def inventory_report(db: Session = Depends(get_db)):
    agent = EnterpriseForecastAgent(db, alert_callback=slack_alert)
    sales = agent.forecast_sales()
    inventory = agent.fetch_inventory_data()
    restock = agent.forecast_inventory()
    report = {}
    router_ids = set(list(sales.keys()) + list(inventory['router_id'].unique()))
    for rid in router_ids:
        report[rid] = {
            "sales_forecast": sales.get(rid).to_dict(orient='records') if sales.get(rid) is not None else [],
            "inventory": inventory[inventory['router_id']==rid].to_dict(orient='records'),
            "restock_suggestions": restock.get(rid, [])
        }
    return report
