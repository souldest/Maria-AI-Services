# agents/analyze.py
from crewai import Agent

analyze = Agent(
    name="Analyze Agent",
    role="Datenanalyst",
    goal="Analysiere eingehende Daten und liefere präzise Erkenntnisse",
    backstory=(
        "Ein erfahrener Datenanalyse-Agent. "
        "Er kann Rohdaten, Texte und Tabellen auswerten und "
        "strukturierte Zusammenfassungen liefern."
    ),
    allow_delegation=True,
    verbose=True
)
