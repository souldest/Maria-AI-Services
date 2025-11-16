# Base image
FROM python:3.11-slim

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend und Frontend Code kopieren
COPY backend ./backend
COPY frontend ./frontend

# Supervisord installieren
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Supervisord Konfig kopieren
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Port freigeben (Streamlit Standardport 8501)
EXPOSE 8501

# Supervisord als Entrypoint starten
CMD ["/usr/bin/supervisord", "-n"]
