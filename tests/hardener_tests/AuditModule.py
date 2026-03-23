import os
import re
from typing import Dict, Union
from pathlib import Path


class SSHAuditor:
    """
    Performs a security audit of the SSH service configuration
    to ensure compliance with system hardening standards.
    """

    # Using Path objects for better cross-platform compatibility
    CONFIG_PATH = Path("/etc/ssh/sshd_config")

    def __init__(self):
        self.audit_results: Dict[str, Union[str, int, bool]] = {}

    def execute_audit(self) -> Dict[str, Union[str, int, bool]]:
        """Orchestrates all security checks on the SSH configuration file."""
        if not self.CONFIG_PATH.exists():
            return {"error": "SSH configuration file not found (FileNotFoundError)"}

        try:
            with open(self.CONFIG_PATH, "r") as f:
                content = f.read()

            # Populating results dictionary with telemetry data
            self.audit_results["current_port"] = self._parse_port(content)
            self.audit_results["port_security_status"] = validate_port_security(
                self.audit_results["current_port"]
            )
            self.audit_results["root_login_allowed"] = self._check_root_login_policy(
                content
            )
            self.audit_results["password_auth_enabled"] = (
                self._check_password_authentication_policy(content)
            )

            return self.audit_results
        except PermissionError:
            return {
                "error": "Insufficient permissions to read SSH config. Run as root/sudo."
            }

    def _parse_port(self, content: str) -> int:
        """Extracts the configured SSH port using regex."""
        match = re.search(r"^Port\s+(\d+)", content, re.MULTILINE)
        return int(match.group(1)) if match else 22

    def _check_root_login_policy(self, content: str) -> bool:
        """Evaluates if the 'PermitRootLogin' policy is set to 'yes'."""
        match = re.search(
            r"^PermitRootLogin\s+yes", content, re.MULTILINE | re.IGNORECASE
        )
        return bool(match)

    def _check_password_authentication_policy(self, content: str) -> bool:
        """Evaluates if password-based authentication is explicitly enabled."""
        match = re.search(
            r"^PasswordAuthentication\s+yes", content, re.MULTILINE | re.IGNORECASE
        )
        return bool(match)


def validate_port_security(port: Union[str, int]) -> bool:
    """Validates if the provided SSH port falls within the recommended non-privileged range."""
    try:
        port_num = int(port)
        # Security best practice: Move SSH to a non-standard, non-privileged port (>1024)
        return 1024 < port_num <= 65535
    except (ValueError, TypeError):
        return False


def modify_config_parameter(content: str, key: str, value: str) -> str:
    """Updates or appends a configuration parameter (Key-Value pair) in a string buffer."""
    pattern = rf"^[#\s]*{key}\s+.*$"
    new_entry = f"{key} {value}"

    if re.search(pattern, content, flags=re.MULTILINE | re.IGNORECASE):
        return re.sub(pattern, new_entry, content, flags=re.MULTILINE | re.IGNORECASE)
    else:
        # Ensuring the file ends with a newline before appending
        return f"{content.rstrip()}\n{new_entry}\n"


def apply_security_remediation(target_port: int = 2222):
    """
    Applies security fixes to the SSH configuration.
    Requires elevated privileges (sudo/root).
    """
    path = "/etc/ssh/sshd_config"

    try:
        with open(path, "r") as f:
            content = f.read()

        # Remediation steps: Change port and disable root login
        updated_content = modify_config_parameter(content, "Port", str(target_port))
        updated_content = modify_config_parameter(
            updated_content, "PermitRootLogin", "no"
        )

        with open(path, "w") as f:
            f.write(updated_content)
        print("Success: Security remediation applied successfully.")

    except PermissionError:
        print("CRITICAL ERROR: Permission denied. Please re-run the script with sudo.")
    except Exception as e:
        print(f"Unexpected error during remediation: {e}")


if __name__ == "__main__":
    auditor = SSHAuditor()
    report = auditor.execute_audit()

    if "error" in report:
        print(f"Audit Failed: {report['error']}")
    else:
        print("--- SSH SECURITY AUDIT REPORT ---")
        for key, value in report.items():
            print(f"{key.replace('_', ' ').upper()}: {value}")

    print("\n--- PORT VALIDATION TEST ---")
    print(f"Is port '2222' secure? {validate_port_security(2222)}")

    # Decision Logic
    user_input = input(
        "\nWould you like to apply security hardening automatically? (y/n): "
    )
    if user_input.lower() == "y":
        apply_security_remediation(target_port=2222)
    else:
        print("Operation aborted. No changes were made to the system.")
