# Base Image
FROM python:3.11-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App kopieren
COPY app/ ./app/

# Expose FastAPI port
EXPOSE 8000

# FastAPI starten
CMD ["uvicorn", "app.routers.forecast_agent:app", "--host", "0.0.0.0", "--port", "8000"]
