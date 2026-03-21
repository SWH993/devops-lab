import os
import re
from typing import Dict, Union
from pathlib import Path

class SSHAuditor:
    """
    Klasa wykonująca audyt bezpieczeństwa usługi SSH.
    """

    CONFIG_PATH = Path("/etc/ssh/sshd_config")

    def __init__(self):
        self.results: Dict[str, Union[str, int, bool]] = {}

    def run_audit(self) -> Dict[str, Union[str, int, bool]]:
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
        """Wyciąga numer portu"""
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
    
def set_config_value(content: str, key: str, value: str) -> str:
    """Uniwersalna funkcja do ustawiania parametrów w plikach typu 'Klucz Wartość'."""
    pattern = rf"^[#\s]*{key}\s+.*$"
    new_line = f"{key} {value}"

    if re.search(pattern, content, flags=re.MULTILINE | re.IGNORECASE):
        return re.sub(pattern, new_line, content, flags=re.MULTILINE | re.IGNORECASE)
    else:
        return f"{content.rstrip()}\n{new_line}\n"

def apply_ssh_fix(new_port: int = 2222):
    path = "/etc/ssh/sshd_config"

    #Odczyt
    with open(path, 'r') as f:
        content = f.read()

    #Modyfikacja
    updated_content = set_config_value(content, "Port", str(new_port))
    updated_content = set_config_value(updated_content, "PermitRootLogin", "no")

    #Zapis (wymaga uprawnień sudo/root)
    try:
        with open(path, 'w') as f:
            f.write(updated_content)
        print("Sukces: Plik konfiguracyjny zaktualizowany.")
    except PermissionError:
        print("BŁĄD: Brak uprawnień do edycji. Uruchom plik przez sudo.")

# --- Uruchomienie ---
if __name__ == "__main__":
    auditor = SSHAuditor()
    raport = auditor.run_audit()

    # Raport
    print("--- RAPORT BEZPIECZEŃSTWA SSH ---")
    for klucz, wartosc in raport.items():
        print(f"{klucz.upper()}: {wartosc}")

    print("\n--- TEST WALIDACJI PORTÓW ---")
    print(f"Czy '2222' jest bezpieczny? {is_port_secure('2222')}")

    stara_konfiguracja = "Port 22\nPermitRootLogin no"
    nowa_konfiguracja = set_config_value(stara_konfiguracja, "Port", "2222")  

    print("\n--- TEST NAPRAWY ---")
    print(f"Przed:\n{stara_konfiguracja}")
    print(f"Po:\n{nowa_konfiguracja}")

    # Decyzja
    decyzja = input("\nCzy chcesz automatycznie naprawić ustawienia SSH? (y/n): ")
    if decyzja.lower() == 'y':
        apply_ssh_fix(new_port=2222)
    else:
        print("Anulowano. Zmiany nie zostały wprowadzone.")