import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

def shutdown_server():
    host = "192.168.1.250"
    user = os.getenv('PM_USER').split('@')[0] # wyciąga 'root' z 'root@pam'
    password = os.getenv('PM_PASS')

    # Tworzy klienta SSH
    client = paramiko.SSHClient()
    # Automatycznie akceptuje klucze 
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"🔌 Łączenie z {host} w celu wyłączenia...")
        client.connect(host, username=user, password=password)
        
        stdin, stdout, stderr = client.exec_command('poweroff')
        
        print("✅ Komenda wyłączenia wysłana. Serwer kończy pracę.")
    except Exception as e:
        print(f"💥 Błąd: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    shutdown_server()