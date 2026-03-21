import psutil
import os
import time
import requests
from dotenv import load_dotenv
from typing import Dict

class Monitor:
    """Klasa wyciągająca dane o CPU, RAM, Dysku i Baterii z hosta Proxmox."""
    
    def __init__(self):
        load_dotenv()
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        if not self.webhook_url:
            print("⚠️ BŁĄD: Brak DISCORD_WEBHOOK_URL w pliku .env")

    def get_cpu(self) -> float:
        return psutil.cpu_percent(interval=1)

    def get_ram(self) -> float:
        return psutil.virtual_memory().percent

    def get_disc(self) -> float:
        return psutil.disk_usage('/').percent
    
    def get_battery(self) -> Dict[str, str]:
        """Pobiera dane o baterii z systemu plików Linuxa."""
        try:
            cap_path = "/sys/class/power_supply/BAT0/capacity"
            stat_path = "/sys/class/power_supply/BAT0/status"

            # Sprawdzenie czy bateria to BAT0 czy BAT1
            if not os.path.exists(cap_path):
                cap_path = cap_path.replace("BAT0", "BAT1")
                stat_path = stat_path.replace("BAT0", "BAT1")

            if not os.path.exists(cap_path):
                return {"capacity": "N/A", "status": "Nie wykryto"}

            with open(cap_path, 'r') as f:
                capacity = f.read().strip()
            with open(stat_path, 'r') as f:
                status = f.read().strip()

            return {"capacity": capacity, "status": status}
        except Exception:
            return {"capacity": "N/A", "status": "Błąd odczytu"}

    def get_stats(self) -> dict:
        """Zbiera wszystkie statystyki w jeden słownik."""
        return {
            "cpu": self.get_cpu(),
            "ram": self.get_ram(),
            "disc": self.get_disc(),
            "battery": self.get_battery()
        }
    
    def send_to_discord(self, stats: dict):
        """Formatuje dane i wysyła je na Webhook Discorda."""
        if not self.webhook_url:
            return
        
        # Bezpieczne pobieranie danych o baterii
        battery = stats.get('battery', {"capacity": "N/A", "status": "Unknown"})
        bat_cap = battery.get('capacity', "N/A")
        bat_status = battery.get('status', "Unknown")

        # Logika koloru (Czerwony jeśli bateria < 20%)
        try:
            is_low = bat_cap != "N/A" and int(bat_cap) < 20
        except ValueError:
            is_low = False
        
        color = 15158332 if is_low else 3066993

        payload = {
            "embeds": [{
                "title": "🖥️ Statystyki Serwera HP - Proxmox",
                "description": "Regularny raport stanu zasobów systemowych hosta.",
                "color": color,
                "fields": [
                    {"name": "🔥 Procesor", "value": f"**{stats['cpu']}%**", "inline": True},
                    {"name": "🧠 Pamięć RAM", "value": f"**{stats['ram']}%**", "inline": True},
                    {"name": "💾 Dysk systemowy", "value": f"**{stats['disc']}%**", "inline": True},
                    {
                        "name": "⚡ Bateria", 
                        "value": f"**{bat_cap}%** ({bat_status})", 
                        "inline": False
                    }
                ],
                "footer": {
                    "text": f"Monitorowanie aktywne • Debian 13 • {time.strftime('%H:%M:%S')}"
                }
            }]
        }

        try:
            res = requests.post(self.webhook_url, json=payload, timeout=10)
            print(f"[{time.strftime('%H:%M:%S')}] Status wysyłki: {res.status_code}")
        except Exception as e:
            print(f"❌ Błąd sieci: {e}")
    
if __name__ == "__main__":
    app = Monitor()
    print("🚀 Monitoring uruchomiony. Raporty co 5 minut...")
    
    while True:
        current_data = app.get_stats()
        app.send_to_discord(current_data)
        time.sleep(300) # 5 minut przerwy