# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# PostgreSQL-Datenbank-URL aus Umgebungsvariable oder Default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://estaghvirou.b@gmail.com:Tochter2026?@maria-ai-service-db.postgres.database.azure.com:5432/postgres?sslmode=require"
)

# Engine für PostgreSQL
engine = create_engine(DATABASE_URL, echo=True)

# Session-Klasse für DB-Zugriffe
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basis-Klasse für Models
Base = declarative_base()

# --- Dependency für FastAPI ---
def get_db():
    """
    Liefert eine SQLAlchemy Session für FastAPI Endpoints.
    Wird via Depends(get_db) verwendet.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
