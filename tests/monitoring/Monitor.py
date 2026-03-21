import psutil
import os
from dotenv import load_dotenv
import requests
from typing import Dict, Optional

class Monitor:
    """Klasa wyciągająca dane o CPU, RAM, Dysku i Baterii z urządzenia."""
    def __init__(self):
        load_dotenv()
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    def get_cpu(self) -> float:
        return psutil.cpu_percent(interval=1)

    def get_ram(self) -> float:
        return psutil.virtual_memory().percent

    def get_disc(self) -> float:
        return psutil.disk_usage('/').percent
    
    def get_battery(self) -> Dict[str, str]:
        try:
            # Ścieżki w Debianie/Proxmoxie dla laptopów
            cap_path = "/sys/class/power_supply/BAT0/capacity"
            stat_path = "/sys/class/power_supply/BAT0/status"

            if not os.path.exists(cap_path):
                cap_path = cap_path.replace("BAT0", "BAT1")
                stat_path = stat_path.replace("BAT0", "BAT1")

            with open(cap_path, 'r') as f:
                capacity = f.read().strip()
            with open(stat_path, 'r') as f:
                status = f.read().strip()

            return {"capacity": capacity, "status": status}
        except FileNotFoundError:
            return {"capacity": "N/A", "status": "Nie wykryto"}

    def get_stats(self):
        cpu = self.get_cpu()
        ram = self.get_ram()
        disc = self.get_disc()
        bat = self.get_battery()

        return {"cpu": cpu, "ram": ram, "disc": disc, "bat": bat}
    
    def send_to_discord(self, stats: dict):
        load_dotenv()
        url = os.getenv('DISCORD_WEBHOOK_URL')

        if not url:
            print("Błąd: Brak Webhook URL w pliku .env")
            return
        
        # Kolor zmienia się na czerwony, jeśli bateria < 20%
        bat_val = stats['battery']['capacity']
        color = 15158332 if bat_val != "N/A" and int(bat_val) < 20 else 3066993

        payload = {
            "embeds": [{
                "title": "🖥️ Statystyki Serwera HP - Proxmox",
                "description": "Regularny raport stanu zasobów systemowych.",
                "color": color,
                "fields": [
                    {
                        "name": "🔥 Procesor",
                        "value": f"**{stats['cpu']}%**",
                        "inline": True
                    },
                    {
                        "name": "🧠 Pamięć RAM",
                        "value": f"**{stats['ram']}%**",
                        "inline": True
                    },
                    {
                        "name": "💾 Dysk systemowy",
                        "value": f"**{stats['disc']}%**",
                        "inline": True
                    },
                    {
                        "name": "⚡ Bateria", 
                        "value": f"{stats['battery']['capacity']}% ({stats['battery']['status']})", 
                        "inline": False}
                ],
                "footer": {
                    "text": "Monitorowanie aktywne • Debian 13"
                }
            }]
        }

        try:
            res = requests.post(self.webhook_url, json=payload)
            print(f"Status wysyłki: {res.status_code}")
        except Exception as e:
            print(f"Błąd sieci: {e}")
    
if __name__ == "__main__":
    app = Monitor()
    
    import time
    while True:
        data = app.get_stats()
        app.send_to_discord(data)
        time.sleep(300) # Raport co 5 minut