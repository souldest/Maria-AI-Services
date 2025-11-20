# Basis-Image mit Python
FROM python:3.11-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Frontend-Code kopieren
COPY . .

# Streamlit Port
EXPOSE 8501

# Startbefehl
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
