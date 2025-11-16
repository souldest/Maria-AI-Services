# ----------------------------------------
# Base Image
# ----------------------------------------
FROM python:3.11-slim

# ----------------------------------------
# Arbeitsverzeichnis im Container
# ----------------------------------------
WORKDIR /app

# ----------------------------------------
# Abhängigkeiten installieren
# ----------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------
# gesamten Code kopieren
# ----------------------------------------
COPY . .

# ----------------------------------------
# Port für Streamlit exposen
# ----------------------------------------
EXPOSE 80

# ----------------------------------------
# Backend (FastAPI) und Frontend (Streamlit) gleichzeitig starten
# ----------------------------------------
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/streamlit_app.py --server.port 80 --server.address 0.0.0.0 --server.headless true"]
