# flows/main_flow.py
from crewai import Crew, Task

# --- Agenten importieren ---
from agents.analyze import analyze
from agents.forecast import forecast
from agents.sales_leads import sales_leads
from agents.kundengewinnung import kundengewinnung
from agents.proposal import proposal
from agents.kunden_support import kunden_support

# --- Tasks definieren ---
analyze_task = Task(
    description="Analysiere die Eingabedaten des Kunden.",
    agent=analyze,
    expected_output="Strukturierte Analyse"
)

forecast_task = Task(
    description="Erstelle Vorhersagen basierend auf der Analyse.",
    agent=forecast,
    depends_on=[analyze_task],
    expected_output="Forecast mit Trends und Zahlen"
)

sales_leads_task = Task(
    description="Erzeuge potenzielle Sales Leads basierend auf der Analyse und Forecast.",
    agent=sales_leads,
    depends_on=[forecast_task],
    expected_output="Liste priorisierter Leads"
)

kundengewinnung_task = Task(
    description="Erstelle Strategien zur Kundengewinnung.",
    agent=kundengewinnung,
    depends_on=[sales_leads_task],
    expected_output="Konkrete Akquise-Strategien"
)

proposal_task = Task(
    description="Erstelle ein professionelles Angebot/Proposal.",
    agent=proposal,
    depends_on=[kundengewinnung_task],
    expected_output="Fertiges Angebot im Textformat"
)

kunden_support_task = Task(
    description="Formuliere eine freundliche Support-Antwort für den Kunden.",
    agent=kunden_support,
    depends_on=[proposal_task],
    expected_output="Support-Antwort"
)

# --- Crew definieren ---
crew = Crew(
    agents=[
        analyze,
        forecast,
        sales_leads,
        kundengewinnung,
        proposal,
        kunden_support
    ],
    tasks=[
        analyze_task,
        forecast_task,
        sales_leads_task,
        kundengewinnung_task,
        proposal_task,
        kunden_support_task
    ],
    verbose=True
)

tracing=True

# --- Flow starten ---
def run_flow(input_text: str):
    """
    Startet den gesamten CrewAI Flow.
    input_text = Kundentext oder Daten, die analysiert werden sollen.
    """
    print("\n🚀 Starte Agenten-Workflow...\n")
    result = crew.kickoff(inputs={"input": input_text})
    print("\n✔️ Workflow abgeschlossen.\n")
    return result


if __name__ == "__main__":
    test_input = "Bitte erstelle ein Angebot für einen Neukunden."
    output = run_flow(test_input)
    print("\n--- Ergebnis ---\n")
    print(output)
