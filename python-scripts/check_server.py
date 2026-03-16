import requests
import urllib3

# Ignorujemy błędy certyfikatu SSL dla lokalnego IP
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# DANE DO TWOJEGO SERWERA
IP = "192.168.1.250"
TOKEN_ID = "root@pam!terraform"
SECRET = "41d159cf-a321-41bf-9458-a9fcd6c62091" 

headers = {
    "Authorization": f"PVEAPIToken={TOKEN_ID}={SECRET}"
}

def get_status():
    url = f"https://{IP}:8006/api2/json/nodes"
    response = requests.get(url, headers=headers, verify=False)
    
    if response.status_code == 200:
        data_list = response.json()['data']
        # Sprawdzamy pierwszy dostępny węzeł (node)
        if data_list:
            node_data = data_list[0]
            print(f"--- STATUS SERWERA: {node_data.get('node', 'Nieznany').upper()} ---")
            
            # Używamy .get(), żeby skrypt nie wywalał się, gdy pola brakuje
            status = node_data.get('status', 'brak danych')
            cpu = node_data.get('cpu', 0) 
            max_mem = node_data.get('maxmem', 1) # Unikamy dzielenia przez zero
            
            print(f"Status: {status}")
            print(f"Obciążenie CPU: {round(cpu * 100, 2)}%")
            print(f"RAM: {round(max_mem / (1024**3), 2)} GB")
        else:
            print("Błąd: API zwróciło pustą listę węzłów.")
    else:
        print(f"Błąd połączenia! Kod statusu: {response.status_code}")
        print(f"Treść odpowiedzi: {response.text}")

if __name__ == "__main__":
    get_status()
