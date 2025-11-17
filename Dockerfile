FROM python:3.12-slim

WORKDIR /app

# Abhängigkeiten kopieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code kopieren
COPY backend ./backend
COPY frontend ./frontend
COPY supervisord.conf .

# Expose Ports
EXPOSE 8000
EXPOSE 8501

CMD ["/usr/bin/supervisord", "-c", "supervisord.conf"]
