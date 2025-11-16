import requests

endpoints = ["/", "/predict", "/forecast"]  # Prüfe, dass hier Werte stehen
base_url = "http://localhost:8000"

for endpoint in endpoints:
    url = f"{base_url}{endpoint}"
    try:
        response = requests.get(url)
        print(f"Endpoint: {endpoint}")
        print(f"Status Code: {response.status_code}")
        print(f"Antwort: {response.text}\n")
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Zugriff auf {endpoint}: {e}\n")
