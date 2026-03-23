import psutil
import os
import time
import requests
from dotenv import load_dotenv
from typing import Dict, Any


class Monitor:
    """
    A telemetry class responsible for extracting resource utilization metrics
    (CPU, RAM, Disk, and Battery) from a Proxmox host.
    """

    def __init__(self):
        load_dotenv()
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        if not self.webhook_url:
            print(
                "⚠️ CONFIGURATION ERROR: DISCORD_WEBHOOK_URL not found in environment variables."
            )

    def get_cpu_utilization(self) -> float:
        """Returns the current CPU usage percentage."""
        return psutil.cpu_percent(interval=1)

    def get_memory_utilization(self) -> float:
        """Returns the percentage of utilized virtual memory."""
        return psutil.virtual_memory().percent

    def get_disk_utilization(self) -> float:
        """Returns the disk space usage percentage for the root directory."""
        return psutil.disk_usage("/").percent

    def get_battery_telemetry(self) -> Dict[str, str]:
        """
        Retrieves battery capacity and status directly from the Linux sysfs interface.
        Supports both BAT0 and BAT1 interfaces.
        """
        try:
            # Standard Linux sysfs paths for power supply monitoring
            base_path = "/sys/class/power_supply/BAT0"
            if not os.path.exists(base_path):
                base_path = base_path.replace("BAT0", "BAT1")

            cap_path = f"{base_path}/capacity"
            stat_path = f"{base_path}/status"

            if not os.path.exists(cap_path):
                return {"capacity": "N/A", "status": "Not Detected"}

            with open(cap_path, "r") as f:
                capacity = f.read().strip()
            with open(stat_path, "r") as f:
                status = f.read().strip()

            return {"capacity": capacity, "status": status}
        except Exception as e:
            return {"capacity": "N/A", "status": f"Read Error: {e}"}

    def collect_metrics(self) -> Dict[str, Any]:
        """Aggregates all system metrics into a single telemetry payload."""
        return {
            "cpu": self.get_cpu_utilization(),
            "ram": self.get_memory_utilization(),
            "disk": self.get_disk_utilization(),
            "battery": self.get_battery_telemetry(),
        }

    def dispatch_to_discord(self, metrics: Dict[str, Any]):
        """
        Formats the collected telemetry data and dispatches it via a Discord Webhook.
        Implements dynamic color-coding based on critical thresholds.
        """
        if not self.webhook_url:
            return

        battery = metrics.get("battery", {})
        bat_cap = battery.get("capacity", "N/A")
        bat_status = battery.get("status", "Unknown")

        # Threshold-based color logic (Red if capacity < 20%)
        try:
            is_low = bat_cap != "N/A" and int(bat_cap) < 20
        except ValueError:
            is_low = False

        # Hex colors: Green (3066993) or Red (15158332)
        embed_color = 15158332 if is_low else 3066993

        payload = {
            "embeds": [
                {
                    "title": "🖥️ HP Server Metrics - Proxmox Host",
                    "description": "Scheduled system resource utilization report.",
                    "color": embed_color,
                    "fields": [
                        {
                            "name": "🔥 CPU Usage",
                            "value": f"**{metrics['cpu']}%**",
                            "inline": True,
                        },
                        {
                            "name": "🧠 RAM Usage",
                            "value": f"**{metrics['ram']}%**",
                            "inline": True,
                        },
                        {
                            "name": "💾 System Disk",
                            "value": f"**{metrics['disk']}%**",
                            "inline": True,
                        },
                        {
                            "name": "⚡ Battery Status",
                            "value": f"**{bat_cap}%** ({bat_status})",
                            "inline": False,
                        },
                    ],
                    "footer": {
                        "text": f"Monitoring Active • Debian 13 • {time.strftime('%H:%M:%S')}"
                    },
                }
            ]
        }

        try:
            response = requests.post(self.webhook_url, json=payload, timeout=15)
            print(
                f"[{time.strftime('%H:%M:%S')}] Dispatch Status: {response.status_code}"
            )
        except requests.exceptions.RequestException as e:
            print(f"❌ Network Exception: {e}")


if __name__ == "__main__":
    monitor = Monitor()
    print("🚀 Monitoring Agent initialized. Dispatching reports every 5 minutes...")

    try:
        while True:
            telemetry_data = monitor.collect_metrics()
            monitor.dispatch_to_discord(telemetry_data)
            time.sleep(300)  # 5-minute polling interval
    except KeyboardInterrupt:
        print("\n🛑 Monitoring Agent terminated by user.")
