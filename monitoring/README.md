# Proxmox Hardware Monitor (Discord Integration)

A lightweight yet robust system resource monitor authored in Python, specifically optimized for Debian 13 / Proxmox environments. It automates telemetry dispatch (CPU, RAM, Disk, and Battery) to Discord channels via Webhooks.

## Key Capabilities

    **Real-time Telemetry**: High-precision monitoring of CPU utilization, memory allocation, and storage overhead using the psutil library.

    **Discord Embed Notifications**: Professional status reports featuring dynamic color-coding based on resource thresholds.

    **Security-First Design**: Fully integrated with .env files to prevent credential exposure (Hardcoded Secrets Mitigation).

    **Scalable Architecture**: Built using Object-Oriented Programming (OOP) principles for maintainability and extensibility.

    **Battery Monitoring**: Integrated support for Linux sysfs to monitor UPS/Battery status on mobile Proxmox nodes.

## Tech Stack

    **Environment**: Python 3.13 (Debian 13 / Trixie)

    **Core Libraries**: psutil, requests, python-dotenv

    **Automation**: Linux Cron Jobs / Systemd Services

    **Communication**: Discord Webhook API (JSON payloads)

## Installation & Configuration

    Clone the repository:
        ```git clone https://github.com/[YOUR_NICK]/devops-lab.git```
        ```cd devops-lab/monitoring```

    Install dependencies:
        ```pip install -r requirements.txt```

    Configure environment variables:
    Create a .env file and define your Webhook URL:
        ```DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...```

    Manual Execution:
        ```python3 Monitor.py```

## Scheduling (Cron)
    To automate the report dispatch every 30 minutes, append the following entry to your crontab -e:
        ```*/30 * * * * /usr/bin/python3 /absolute/path/to/Monitor.py```

This project was developed as part of a comprehensive DevOps & Linux Automation learning path, focusing on system reliability and infrastructure monitoring.