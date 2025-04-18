import requests
import os
from dotenv import load_dotenv
# --- Cargar .env (recomendado para client_id y client_secret) ---
load_dotenv()
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
CODE_CALENDAR = os.environ["CODE_CALENDAR"]

# URL para obtener el token
TOKEN_URL = "https://oauth2.googleapis.com/token"

# Datos necesarios
payload = {
    "client_id": CLIENT_ID,  # Reemplaza con tu CLIENT_ID
    "client_secret": CLIENT_SECRET,  # Reemplaza con tu CLIENT_SECRET
    "code": CODE_CALENDAR,  # Reemplaza con el código obtenido
    "grant_type": "authorization_code",
    "redirect_uri": "http://localhost:8000/callback"  # Asegúrate de que coincida con tu configuración
}

# Solicitar el token
response = requests.post(TOKEN_URL, data=payload)
if response.status_code == 200:
    token_info = response.json()
    access_token = token_info.get("access_token")
    print(f"Access Token: {access_token}")
else:
    print(f"Error: {response.status_code} - {response.text}")
