# DevOps Lab Automation - Proxmox Control

Projekt automatyzacji domowego laboratorium opartego na systemie **Proxmox** oraz **Debian 13**. Skrypt pozwala na zdalne zarządzanie zasilaniem serwera głównego oraz przygotowuje grunt pod automatyczny pipeline postów na Instagram.

## 🚀 Funkcjonalności
- **Wake on LAN (WoL):** Skrypt Python do zdalnego budzenia serwera za pomocą pakietów Magic Packet.
- **SSH Remote Shutdown:** Bezpieczne wyłączanie serwera poprzez protokół SSH.
- **Security First:** Pełna integracja z plikami `.env` w celu ochrony haseł i adresów MAC (pliki te są ignorowane przez Git).
- **Python venv:** Wykorzystanie wirtualnych środowisk dla zachowania czystości systemu Debian 13.

## 🛠️ Technologie
- **Python 3.11+**
- **Libraries:** `paramiko`, `python-dotenv`, `wakeonlan`
- **OS:** Debian 13 (Trixie)
- **Infrastructure:** Proxmox VE

## 📋 Instalacja i konfiguracja

1. **Klonowanie repozytorium:**
   ```bash
   git clone git@github.com:TWOJ_NICK/devops-lab.git
   cd devops-lab

Przygotowanie środowiska:
    Bash

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    Konfiguracja zmiennych:
    Utwórz plik .env i uzupełnij dane:
    Plaintext

    PM_API_URL=https://<IP_PROXMOXA>:8006/api2/json
    PM_USER=root@pam
    PM_PASS=twoje_haslo
    SRV_MAC=AA:BB:CC:DD:EE:FF

🕹️ Użycie

    Włączanie serwera: python3 wol_start.py

    Wyłączanie serwera: python3 srv_off.py

📅 Plan rozwoju (Roadmap)

    [ ] Implementacja automatycznego sprawdzania statusu (ping) po wysłaniu WoL.

    [ ] Izolacja sieciowa maszyn wirtualnych (Firewall Proxmox).

    [ ] Pipeline do automatycznego generowania i publikowania treści na Instagram.