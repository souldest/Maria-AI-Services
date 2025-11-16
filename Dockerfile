# ------------------------------
# Basis-Image
# ------------------------------
FROM python:3.11-slim

# ------------------------------
# Arbeitsverzeichnis
# ------------------------------
WORKDIR /app

# ------------------------------
# Abhängigkeiten kopieren und installieren
# ------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------------
# Applikation kopieren
# ------------------------------
COPY backend ./backend
COPY frontend ./frontend
COPY supervisord.conf ./supervisord.conf

# ------------------------------
# Logs-Verzeichnis
# ------------------------------
RUN mkdir -p /app/logs

# ------------------------------
# Supervisord als Entrypoint
# ------------------------------
CMD ["supervisord", "-c", "/app/supervisord.conf"]
