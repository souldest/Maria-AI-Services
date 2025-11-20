# =========================
# Stage 1: Builder
# =========================
FROM python:3.10-bullseye AS builder

# Arbeitsverzeichnis
WORKDIR /app

# Systemabhängigkeiten für Pakete wie prophet, scikit-learn
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev gcc g++ git && \
    rm -rf /var/lib/apt/lists/*

# Requirements kopieren und Pakete installieren
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefer-binary --user -r requirements.txt

# =========================
# Stage 2: Final Image
# =========================
FROM python:3.10-slim

WORKDIR /app

# User-Installierte Pakete aus Builder kopieren
COPY --from=builder /root/.local /root/.local

# Code kopieren
COPY . .

# PATH anpassen, damit pip user-installierte Pakete gefunden werden
ENV PATH=/root/.local/bin:$PATH

# .env kopieren (falls nötig)
COPY .env .env

# Port setzen
EXPOSE 8002

# Startbefehl
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
