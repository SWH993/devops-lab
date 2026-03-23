import os
import time
import paramiko
from dotenv import load_dotenv

load_dotenv()


def execute_graceful_hibernation():
    """
    Orchestrates a multi-stage hibernation sequence:
    1. Dispatches a final status report via Discord.
    2. Gracefully terminates all active Virtual Machines and Containers.
    3. Triggers system-level hibernation on the Proxmox host.
    """
    host = "192.168.1.250"
    # Extracting the username from PVE format (e.g., 'root@pam' -> 'root')
    raw_user = os.getenv("PM_USER")
    username = raw_user.split("@")[0] if raw_user else "root"
    password = os.getenv("PM_PASS")

    # Initializing the SSH client with an automated host key policy
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"🔌 Establishing secure connection to {host}...")
        ssh_client.connect(host, username=username, password=password, timeout=10)

        # PHASE 1: Final Telemetry Dispatch
        # Executing the monitoring script once before shutdown for visibility
        print("Dispatching final telemetry report to Discord...")
        ssh_client.exec_command("python3 /root/scripts/Monitor.py --once")

        # Allow a short buffer for the network packet to reach the webhook
        time.sleep(5)

        # PHASE 2: Graceful Termination of Guest Systems
        print("Terminating all Virtual Machines and LXC containers...")
        # 'qm stopall' handles VMs; the loop ensures all LXC containers are halted
        termination_cmd = 'qm stopall && for ct in $(pct list | awk "NR>1 {print $1}"); do pct stop $ct; done'
        ssh_client.exec_command(termination_cmd)

        # Buffer for disk I/O to flush and guest OS to halt completely
        time.sleep(7)

        # PHASE 3: System-Level Hibernation
        print("Initiating system hibernation sequence...")
        # Executing in the background to prevent SSH hang-ups during power transition
        ssh_client.exec_command("systemctl hibernate &")

        print("Orchestrated hibernation sequence completed successfully.")

    except Exception as e:
        print(f"Critical Error during hibernation sequence: {e}")
    finally:
        ssh_client.close()


if __name__ == "__main__":
    execute_graceful_hibernation()
