import psutil
import os
from dotenv import load_dotenv
import requests
from typing import Dict

class Monitor:
    """Klasa wyciągająca dane o CPU, RAM i Dysku z urządzenia."""
    def __init__(self):
            pass

    def get_cpu(self) -> float:
        return psutil.cpu_percent(interval=1)

    def get_ram(self) -> float:
        return psutil.virtual_memory().percent

    def get_disc(self) -> float:
        return psutil.disk_usage('/').percent

    def get_stats(self):
        cpu = self.get_cpu()
        ram = self.get_ram()
        disc = self.get_disc()

        print(f"CPU: {cpu}%")
        print(f"RAM: {ram}%")
        print(f"DISC: {disc}%")

        return {"cpu": cpu, "ram": ram, "disk": disc}
    
    def send_to_discord(self, stats: dict):
        load_dotenv()
        url = os.getenv('DISCORD_WEBHOOK_URL')

        payload = {
            "content": f"**Raport z Proxmox**\nCPU: {stats['cpu']}%\nRAM: {stats['ram']}%\nDisk: {stats['disk']}%"
        }

        message = requests.post(url, json=payload)

        print(f"Status wysyłki: {message.status_code}")
    
if __name__ == "__main__":
    app = Monitor()
    
    message_to_discord = app.get_stats()
    app.send_to_discord(message_to_discord)