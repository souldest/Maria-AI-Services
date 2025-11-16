import requests

BASE_URL = "http://localhost:8000/forecast"

def test_root_endpoint():
    resp = requests.get("http://localhost:8000/")
    print("Root Endpoint:")
    print("Status Code:", resp.status_code)
    try:
        print("Antwort:", resp.json(), "\n")
    except Exception as e:
        print("Fehler beim JSON-Parsing:", e, "\n")

def test_sales_forecast():
    resp = requests.get(f"{BASE_URL}/sales")
    print("Sales Forecast Endpoint:")
    print("Status Code:", resp.status_code)
    try:
        data = resp.json()
        print("Beispiel Router Forecast:", list(data.items())[:1])
    except Exception as e:
        print("Fehler beim JSON-Parsing:", e)

def test_inventory_forecast():
    resp = requests.get(f"{BASE_URL}/inventory")
    print("Inventory Forecast Endpoint:")
    print("Status Code:", resp.status_code)
    try:
        data = resp.json()
        print("Beispiel Router Inventory Forecast:", list(data.items())[:1])
    except Exception as e:
        print("Fehler beim JSON-Parsing:", e)

def test_inventory_report():
    resp = requests.get(f"{BASE_URL}/inventory-report")
    print("Inventory Report Endpoint:")
    print("Status Code:", resp.status_code)
    try:
        data = resp.json()
        print("Beispiel Router Inventory Report:", list(data.items())[:1])
    except Exception as e:
        print("Fehler beim JSON-Parsing:", e)

if __name__ == "__main__":
    test_root_endpoint()
    test_sales_forecast()
    test_inventory_forecast()
    test_inventory_report()

