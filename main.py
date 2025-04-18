from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import os.path
import json

# Autenticación con Google
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        #try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        #except Exception as e:
        #    print(e)
        #if not creds or not creds.valid:
        #    if creds and creds.expired and creds.refresh_token:
        #        creds.refresh(Request())
        #    else:
        #        flow = InstalledAppFlow.from_client_secrets_file('token.json', SCOPES)
        #        creds = flow.run_local_server(port=0)
        #    with open('token.json', 'w') as token:
        #        token.write(creds.to_json())
    return creds

def create_event():
    service = build('calendar', 'v3', credentials=authenticate_google())

    # Datos del evento
    event = {
        'summary': 'Título de la tarea',  # Título
        'location': 'Lugar de la reunión',  # Ubicación
        'description': 'Descripción del evento',  # Descripción
        'start': {
            'dateTime': '2025-04-20T09:00:00-05:00',  # Fecha y hora de inicio
            'timeZone': 'America/Lima',  # Zona horaria
        },
        'end': {
            'dateTime': '2025-04-20T10:00:00-05:00',  # Fecha y hora de fin
            'timeZone': 'America/Lima',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # Recordatorio por correo electrónico
                {'method': 'popup', 'minutes': 10},  # Recordatorio emergente
            ],
        },
    }

    # Inserta el evento en el calendario
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print('Evento creado:', event_result['htmlLink'])

# Ejecuta la función
if __name__ == '__main__':
    create_event()
