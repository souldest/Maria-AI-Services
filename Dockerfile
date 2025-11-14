# Base Image
FROM python:3.11-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App kopieren (inkl. routers & services)
COPY app/ ./app/

# Streamlit-Port
EXPOSE 8501

# Streamlit starten (headless)
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.headless=true"]
