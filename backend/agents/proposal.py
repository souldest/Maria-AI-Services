# agents/proposal.py
from crewai import Agent

proposal = Agent(
    name="Proposal Agent",
    role="Angebotserstellung",
    goal="Erstelle professionelle Angebote basierend auf den Kunden- und Sales-Daten",
    backstory=(
        "Erfahrener Proposal-Agent, spezialisiert auf präzise Angebote "
        "für Kunden basierend auf analysierten Daten und Leads."
    ),
    allow_delegation=True,
    verbose=True
)
