# DevOps Lab Automation - Proxmox Control

comprehensive automation suite designed for a home-lab environment running on **Proxmox VE** and **Debian 13 (Trixie)**. This project enables remote power management and establishes the foundation for an automated Instagram content pipeline.

## Key Capabilities
- **Wake on LAN (WoL):** Python-based utility to trigger remote boot sequences via Magic Packets.
- **SSH Remote Shutdown:** Orchestrated graceful shutdown/hibernation via the SSH protocol.
- **Security First:** Full integration with `.env` variables to safeguard credentials and hardware addresses (all secrets are git-ignored).
- **Python venv Isolation:** Deployment within virtual environments to maintain the integrity of the Debian 13 host system.
- **SSH Security Auditor:** An automated module that performs deep-scan audits of SSH configurations (port analysis, root login policies, and authentication methods).
- **Auto-Fixing Engine:** Intelligent system file modification `(/etc/ssh/sshd_config)` leveraging advanced Regular Expressions (Regex).
- **Safe Port Validation:** Logic-based security checks for non-standard port ranges (1024-65535) with integrated exception handling.
- **Modular Architecture:** Fully decoupled, Object-Oriented design (`SSHAuditor` class) ready for integration into larger infrastructure frameworks.

## Tech Stack
- **Python 3.11+**
- **Libraries:** `paramiko`, `python-dotenv`, `wakeonlan`, `psutil`, `requests`
- **OS:** Debian 13 (Trixie)
- **Infrastructure:** Proxmox VE

## Installation & Configuration

1. **Clone the repository:**
    ```git clone git@github.com:YOUR_NICK/devops-lab.git
    cd devops-lab```

2. **Environment Initialization:**
    ```python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt```

    **Credential Setup:**
    Create a .env file in the root directory and populate it with your environment details:
        ```PM_API_URL=https://<IP_PROXMOXA>:8006/api2/json
        PM_USER=root@pam
        PM_PASS=twoje_haslo
        SRV_MAC=AA:BB:CC:DD:EE:FF```

3. **System Permissions:**
    Note: Certain modules (e.g., AuditModule.py) require elevated privileges (sudo) to access and modify protected system files:
        ```sudo venv/bin/python AuditModule.py```

    **Usage Guide**
    * Initiate Boot (WoL): `python3 wol_start.py`
    * Remote Shutdown: `python3 srv_off.py`
    * Security Audit/Hardening: `sudo ./venv/bin/python AuditModule.py`

📅 **Development Roadmap**

    [x] **SSH Hardening**: Automated port migration and root login restriction.

    [x] **Battery & Resource Monitor**: Battery & Resource monitoring script with Discord Webhook integration.

    [x] **Proxmox Network Isolation**: Implementing VLAN/Bridge/Firewall rules for VM segmenting.

    [ ] **Instagram Pipeline**: Content automation (Shorts/Posts) leveraging Python's media libraries.