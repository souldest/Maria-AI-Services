# agents/sales_leads.py
from crewai import Agent

sales_leads = Agent(
    name="Sales Leads Agent",
    role="Lead-Generierungsspezialist",
    goal="Generiere hochwertige Sales Leads basierend auf Analyse und Forecast",
    backstory=(
        "Erfahrener Sales-Agent, spezialisiert auf Lead-Identifikation "
        "und Priorisierung."
    ),
    allow_delegation=True,
    verbose=True
)
