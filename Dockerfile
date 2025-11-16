# Base Image
FROM python:3.11-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Abhängigkeiten kopieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend & Frontend Code kopieren
COPY backend ./backend
COPY frontend ./frontend

# Supervisord installieren, um mehrere Prozesse zu starten
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Supervisord Konfig kopieren
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose Ports
EXPOSE 8000 8501

# Starten
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
