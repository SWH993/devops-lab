import requests
import urllib3

# Ignore SSL certificate warnigns for local IP
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# SERVER DATA
IP = "<IP_ADDRESS>"
TOKEN_ID = "root@pam!mytokenid"
SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

headers = {"Authorization": f"PVEAPIToken={TOKEN_ID}={SECRET}"}


def get_status():
    url = f"https://{IP}:8006/api2/json/nodes"
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        data_list = response.json()["data"]
        # first node check
        if data_list:
            node_data = data_list[0]
            print(f"--- SERVER STATUS: {node_data.get('node', 'Unknown').upper()} ---")

            # Use .get() to avoid KeyError if fields are missing
            status = node_data.get("status", "no data")
            cpu = node_data.get("cpu", 0)
            max_mem = node_data.get("maxmem", 1)  # Avoid division by zero

            print(f"Node status: {status}")
            print(f"CPU load: {round(cpu * 100, 2)}%")
            print(f"RAM: {round(max_mem / (1024**3), 2)} GB")
        else:
            print("Error: API returned an empty list of nodes.")
    else:
        print(f"Error connecting! Status code: {response.status_code}")
        print(f"Response content: {response.text}")


if __name__ == "__main__":
    get_status()
