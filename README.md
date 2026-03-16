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