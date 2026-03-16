import os
import sys
from dotenv import load_dotenv
from wakeonlan import send_magic_packet

def wake_server():
    # Ładowanie zmiennych z pliku .env
    load_dotenv()
    
    mac = os.getenv('SRV_MAC')
    
    if not mac:
        print("❌ BŁĄD: Nie znaleziono SRV_MAC w pliku .env!")
        sys.exit(1)

    try:
        print(f"🚀 Wysyłam Magic Packet do: {mac}...")
        send_magic_packet(mac)
        print("✅ Pakiet wysłany pomyślnie!")
        print("💡 Poczekaj około 1-2 minuty, aż serwer wstanie i ping zacznie odpowiadać.")
    except Exception as e:
        print(f"💥 Coś poszło nie tak: {e}")

if __name__ == "__main__":
    wake_server()