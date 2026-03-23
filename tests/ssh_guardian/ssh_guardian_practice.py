import paramiko
import socket
import subprocess
import os
from dotenv import load_dotenv


def check_server_status(ip):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", ip], capture_output=True, text=True, timeout=2
        )

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def secure_ssh_connect(host, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    is_alive = check_server_status(host)

    if is_alive:
        print("Server okay, attempting SSH connection...")
    else:
        print("Server is down.")

    try:
        print(f"Connecting to {host}...")
        client.connect(hostname=host, username=username, password=password, timeout=5)

        return "Successfully connected!"

    except paramiko.AuthenticationException:
        return "Error: Incorrect password or username!"
    except socket.timeout:
        return "Error: Server did not respond in time (Timeout)!"
    except Exception as e:
        return f"Unexpected error: {e}"
    finally:
        client.close()


# TEST
if __name__ == "__main__":
    load_dotenv()

    MY_IP = os.getenv("PROXMOX_IP")
    MY_USER = os.getenv("PROXMOX_USER")
    MY_PASSWORD = os.getenv("PROXMOX_PASS")
    result = secure_ssh_connect(MY_IP, MY_USER, MY_PASSWORD)
    print(result)
