import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("PM_API_URL")
user = os.getenv("PM_USER")
password = os.getenv("PM_PASS")

print("--- CONNECTING TO PROXMOX API ---")
print(f"URL: {url}")
print(f"User: {user}")

if password:
    print("Password: Loaded successfully")
else:
    print("Password: ERROR! Password not found in .env file")
