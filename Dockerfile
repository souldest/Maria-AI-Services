# Stage 1: Backend
FROM python:3.11-slim AS backend
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .

# Stage 2: Frontend
FROM python:3.11-slim AS frontend
WORKDIR /app/frontend
COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY frontend/ .

# Stage 3: Final image mit Nginx
FROM nginx:alpine
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Copy backend & frontend
COPY --from=backend /app/backend /app/backend
COPY --from=frontend /app/frontend /app/frontend

# Install Supervisor, um mehrere Prozesse zu starten
RUN apk add --no-cache python3 py3-pip supervisor \
    && pip install uvicorn streamlit

COPY supervisord.conf /etc/supervisord.conf

EXPOSE 80
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
