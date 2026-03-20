import os
import re
from typing import Dict, Union

class SSHAuditor:
    """
    Klasa wykonująca audyt bezpieczeństwa usługi SSH.
    """

    CONFIG_PATH = "/etc/ssh/sshd_config"

    def __init__(self):
        self.results: Dict[str, Union[str, int, bool]] = {}

    def run_audit(self) => Dict[str, Union[str, int, bool]]:
        """uruchamia wszytskie testy audytowe"""
        if not os.path.exists(self.CONFIG_PATH):
            return {"error": "Brak pliku konfiguracji SSH"}

        with open(self.CONFIG_PATH, 'r') as f:
            content = f.read()

        self.results['port'] = self._check_port(content)
        self.results['is_port_safe'] = is_port_secure(self.results['port'])
        self.results['root_login'] = self._check_root_login(content)
        self.results['password_auth'] = self._check_password_auth(content)
        
        return self.results

    def _check_port(self, content: str) -> int:
        """Wyciąga numer portu za pomocą wyrażeń regularnych (Regex)."""
        match = re.search(r"^Port\s+(\d+)", content, re.MULTILINE)
        return int(match.group(1)) if match else 22

    def _check_root_login(self, content: str) -> bool:
        """Sprawdza, czy PermitRootLogin jest ustawione na 'yes'."""
        match = re.search(r"^PermitRootLogin\s+yes", content, re.MULTILINE)
        return True if match else False

    def _check_password_auth(self, content: str) -> bool:
        """Sprawdza, czy PasswordAuthentication jest włączone."""
        match = re.search(r"^PasswordAuthentication\s+yes", content, re.MULTILINE)
        return True if match else False

def is_port_secure(port: any) -> bool:
    """Sprawdza, czy podany port SSH jest poprawny i bezpieczny."""
    try:
        port_num = int(port)
        return 1024 < port_num < 65535
    except (ValueError, TypeError):
        return False

# --- Uruchomienie ---
if __name__ == "__main__":
    auditor = SSHAuditor()
    raport = auditor.run_audit()

    print("--- RAPORT BEZPIECZEŃSTWA SSH ---")
    for klucz, wartosc in raport.items():
        print(f"{klucz.upper()}: {wartosc}")

    print("\n--- TEST WALIDACJI PORTÓW ---")
    print(f"Czy '2222' jest bezpieczny? {is_port_secure('2222')}")
    print(f"Czy 'xxxx' jest bezpieczny? {is_port_secure('xxxx')}")