from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Definir los alcances necesarios
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Iniciar el flujo de autenticación
flow = InstalledAppFlow.from_client_secrets_file(
    'token_calendarios.json', SCOPES,redirect_uri='http://localhost:8000/')
credentials = flow.run_local_server(port=8000)

# Guardar las credenciales en un archivo token.json
with open('token.json', 'w') as token:
    token.write(credentials.to_json())
