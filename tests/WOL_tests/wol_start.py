import os
import sys
from dotenv import load_dotenv
from wakeonlan import send_magic_packet
from typing import Optional


def initiate_remote_boot():
    """
    Triggers a remote boot sequence by dispatching a Magic Packet
    to the target hardware address (MAC).
    """
    # Loading environment variables for sensitive hardware data
    load_dotenv()

    mac_address: Optional[str] = os.getenv("SRV_MAC")

    if not mac_address:
        print("CONFIGURATION ERROR: 'SRV_MAC' not found in environment variables.")
        sys.exit(1)

    try:
        print(f"Dispatching Magic Packet to: {mac_address}...")

        # Transmission of the WoL packet across the local network
        send_magic_packet(mac_address)

        print("Packet transmitted successfully.")
        print(
            "Note: Please allow 1-2 minutes for the system to initialize and respond to ICMP (ping)."
        )
    except Exception as e:
        print(f"Transmission Failure: An unexpected error occurred: {e}")


if __name__ == "__main__":
    initiate_remote_boot()
