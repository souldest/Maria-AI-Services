# agents/kundengewinnung.py
from crewai import Agent

kundengewinnung = Agent(
    name="Kundengewinnung Agent",
    role="Akquise-Spezialist",
    goal="Formuliere Strategien zur Kundengewinnung basierend auf den Sales Leads",
    backstory=(
        "Experte für Kundenakquise und Outreach-Strategien. "
        "Kann Leads in potenzielle Kunden umwandeln und priorisieren."
    ),
    allow_delegation=True,
    verbose=True
)

