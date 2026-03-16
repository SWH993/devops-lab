import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('PM_API_URL')
user = os.getenv('PM_USER')
password = os.getenv('PM_PASS')

print("--- Test połączenia ---")
print(f"URL: {url}")
print(f"Użytkownik: {user}")

if password:
    print("Hasło: Wczytano poprawnie")
else:
    print("Hasło: BŁĄD! Nie znaleziono hasła w pliku .env")