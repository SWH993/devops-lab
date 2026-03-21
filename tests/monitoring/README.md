# 🖥️ Proxmox Hardware Monitor (Discord Integration)

Prosty, ale potężny monitor zasobów systemowych napisany w Pythonie, zaprojektowany do działania na serwerach Debian/Proxmox. Automatycznie wysyła status CPU, RAM i Dysku na kanał Discord za pomocą Webhooków.

## 🚀 Funkcje
* **Real-time Monitoring**: Pobieranie danych o zużyciu procesora, pamięci operacyjnej i dysku za pomocą biblioteki `psutil`.
* **Discord Alerts**: Profesjonalne powiadomienia typu Embed z kolorami statusu.
* **DevOps Ready**: Pełna integracja z plikami `.env` (bezpieczeństwo haseł) oraz harmonogramem `cron`.
* **Clean Code**: Architektura oparta na klasach (Python OOP).

## 🛠️ Technologie
* **Język**: Python 3.13 (Debian 13)
* **Biblioteki**: `psutil`, `requests`, `python-dotenv`
* **Automatyzacja**: Linux Cron Jobs
* **Komunikacja**: Discord Webhooks (JSON API)

## 📦 Instalacja i Konfiguracja

1. **Sklonuj repozytorium:**
   git clone [https://github.com/](https://github.com/)[TWOJ_NICK]/devops-lab.git
   cd devops-lab/tests/monitoring

2. **Zainstaluj zależności:**
    pip install -r requirements.txt

3. **Skonfiguruj zmienne środowiskowe:**
    Utwórz plik .env i dodaj swój Webhook:
    Fragment kodu

    DISCORD_WEBHOOK_URL=[https://discord.com/api/webhooks/](https://discord.com/api/webhooks/)...

4.  **Uruchom testowo:**
    python3 Monitor.py

**⏰ Automatyzacja (Cron)**
    Aby skrypt uruchamiał się co 30 minut, dodaj poniższą linię do crontab -e:
    */30 * * * * /sciezka/do/python3 /sciezka/do/Monitor.py

Projekt stworzony w ramach nauki DevOps i automatyzacji systemów Linux.