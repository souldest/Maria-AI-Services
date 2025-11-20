# agent/forecast_agent.py
import os
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd
from prophet import Prophet
import numpy as np

# Datenbank-Verbindung
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


class EnterpriseForecastAgent:
    """
    Enterprise-ready Forecast Agent für Umsatz & Vorrat.
    Features:
    - Prophet Zeitreihenprognose
    - Lagerhistorie berücksichtigt
    - Dynamische Sicherheitsbestände
    - Warnungen & Nachbestellvorschläge
    """

    def __init__(self, base_safety_stock: int = 5, forecast_days: int = 14, alert_callback=None):
        self.engine = engine
        self.base_safety_stock = base_safety_stock
        self.forecast_days = forecast_days
        self.alert_callback = alert_callback  # z.B. Funktion zum Versenden von Alerts

    def fetch_sales_data(self) -> pd.DataFrame:
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT router_id, amount, created_at
                FROM sales
                ORDER BY created_at ASC
            """))
            data = [dict(row) for row in result]
        df = pd.DataFrame(data)
        if not df.empty:
            df['created_at'] = pd.to_datetime(df['created_at'])
        return df

    def fetch_inventory_data(self) -> pd.DataFrame:
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT router_id, product_name, stock_level
                FROM inventory
            """))
            data = [dict(row) for row in result]
        return pd.DataFrame(data)

    def forecast_sales(self) -> Dict[int, pd.DataFrame]:
        """Forecast per router using Prophet."""
        df = self.fetch_sales_data()
        forecasts = {}

        for rid, group in df.groupby('router_id'):
            ts = group.groupby('created_at')['amount'].sum().reset_index()
            ts.rename(columns={'created_at': 'ds', 'amount': 'y'}, inplace=True)

            if len(ts) < 3:
                # Zu wenig Daten für Prophet → Mittelwert
                ts_future = pd.DataFrame({
                    'ds': [datetime.now() + timedelta(days=i) for i in range(self.forecast_days)],
                    'yhat': [ts['y'].mean() if len(ts) > 0 else 0] * self.forecast_days,
                    'yhat_lower': [0] * self.forecast_days,
                    'yhat_upper': [0] * self.forecast_days
                })
            else:
                model = Prophet(daily_seasonality=True, weekly_seasonality=True, yearly_seasonality=True)
                model.fit(ts)
                future = model.make_future_dataframe(periods=self.forecast_days)
                forecast = model.predict(future)
                ts_future = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(self.forecast_days)

            forecasts[rid] = ts_future

        return forecasts

    def generate_restock_suggestions(self) -> Dict[int, List[Dict]]:
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

    def summary_report(self) -> Dict[int, Dict]:
        """Zusammenfassender Enterprise-Report pro Router."""
        sales_forecasts = self.forecast_sales()
        inventory_df = self.fetch_inventory_data()
        restock = self.generate_restock_suggestions()

        report = {}
        router_ids = set(list(sales_forecasts.keys()) + list(inventory_df['router_id'].unique()))
        for rid in router_ids:
            forecast_df = sales_forecasts.get(rid)
            forecast_list = forecast_df.to_dict(orient='records') if forecast_df is not None else []
            inventory_list = inventory_df[inventory_df['router_id'] == rid].to_dict(orient='records')
            report[rid] = {
                "sales_forecast": forecast_list,
                "inventory": inventory_list,
                "restock_suggestions": restock.get(rid, [])
            }

        return report


# Beispiel für einen Alert-Callback
def slack_alert(router_id, product_name, current_stock, reorder_qty):
    print(f"[ALERT] Router {router_id}, Produkt {product_name} niedrig: {current_stock} Stück, Nachbestellung: {reorder_qty}")
