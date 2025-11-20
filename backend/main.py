from fastapi import FastAPI, Depends
from pydantic import BaseModel

# CrewAI Agents Imports
from agents.analyze import analyze
from agents.forecast import forecast
from agents.sales_leads import sales_leads
from agents.kundengewinnung import kundengewinnung
from agents.proposal import proposal
from agents.kunden_support import kunden_support  # <-- hinzugefügt

# Flow Import
from flows.main_flow import run_flow

# Database
from database.db import SessionLocal
from database.crud import log_agent

app = FastAPI(title="Agenten Backend API")


# Dependency → liefert DB-Session per Request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic-Modell für Input
class InputData(BaseModel):
    text: str


@app.get("/")
def root():
    return {"status": "Backend läuft!"}


@app.post("/run")
def run_agents(data: InputData, db=Depends(get_db)):
    # Flow ausführen
    result = run_flow(data.text)

    # Logging in Datenbank
    log_agent(
        db,
        agent_name="main_flow",
        input_text=data.text,
        output_text=str(result)
    )

    return {"result": str(result)}
