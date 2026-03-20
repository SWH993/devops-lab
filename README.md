# DevOps Lab Automation - Proxmox Control

Projekt automatyzacji domowego laboratorium opartego na systemie **Proxmox** oraz **Debian 13**. Skrypt pozwala na zdalne zarządzanie zasilaniem serwera głównego oraz przygotowuje grunt pod automatyczny pipeline postów na Instagram.

## 🚀 Funkcjonalności
- **Wake on LAN (WoL):** Skrypt Python do zdalnego budzenia serwera za pomocą pakietów Magic Packet.
- **SSH Remote Shutdown:** Bezpieczne wyłączanie serwera poprzez protokół SSH.
- **Security First:** Pełna integracja z plikami `.env` w celu ochrony haseł i adresów MAC (pliki te są ignorowane przez Git).
- **Python venv:** Wykorzystanie wirtualnych środowisk dla zachowania czystości systemu Debian 13.
- **SSH Security Auditor:** Autorski moduł w Pythonie wykonujący audyt bezpieczeństwa plików konfiguracyjnych SSH (port, logowanie roota, autoryzacja hasłem).
- **Auto-Fixing Engine:** Inteligentna funkcja modyfikacji plików systemowych (`/etc/ssh/sshd_config`) z wykorzystaniem zaawansowanych wyrażeń regularnych (Regex).
- **Safe Port Validation:** Logika walidująca bezpieczeństwo portów (zakres 1024-65535) z obsługą błędów typu `try-except`.
- **Modular Architecture:** Kod podzielony na klasy (`SSHAuditor`) i uniwersalne funkcje pomocnicze, gotowy do importowania w większych systemach.

## 🛠️ Technologie
- **Python 3.11+**
- **Libraries:** `paramiko`, `python-dotenv`, `wakeonlan`, `psutil`, `requests`
- **OS:** Debian 13 (Trixie)
- **Infrastructure:** Proxmox VE

## 📋 Instalacja i konfiguracja

1. **Klonowanie repozytorium:**
    git clone git@github.com:TWOJ_NICK/devops-lab.git
    cd devops-lab

2. **Przygotowanie środowiska:**
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    **Konfiguracja zmiennych:**
    Utwórz plik .env i uzupełnij dane:
        PM_API_URL=https://<IP_PROXMOXA>:8006/api2/json
        PM_USER=root@pam
        PM_PASS=twoje_haslo
        SRV_MAC=AA:BB:CC:DD:EE:FF

3. **Uprawnienia systemowe:**
    Niektóre moduły (np. AuditModule) wymagają uprawnień administratora do odczytu/zapisu plików systemowych:
        sudo venv/bin/python AuditModule.py

🕹️ **Użycie**
    * Włączanie serwera: python3 wol_start.py
    * Wyłączanie serwera: python3 srv_off.py
    * Audyt/Hardening SSH: sudo ./venv/bin/python AuditModule.py

📅 **Plan rozwoju (Roadmap)**

    [x] SSH Hardening: Automatyczna zmiana portu i blokada logowania na roota.

    [ ] Battery & Resource Monitor: Skrypt wysyłający stan baterii laptopa i zużycie zasobów Proxmoxa na Discorda (Webhook).

    [ ] Proxmox Network Isolation: Izolacja maszyn wirtualnych od sieci lokalnej (VLAN/Bridge/Firewall).

    [ ] Instagram Pipeline: Automatyzacja treści (Shorts/Posts) przy użyciu Pythona.