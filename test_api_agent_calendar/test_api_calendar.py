import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def eliminar_evento_google_calendar(
    event_id: str,
    token_file: str = "token.json",
    calendar_id: str = "primary"
):
    """
    Elimina un evento de Google Calendar por su event_id.
    """
    # Cargar credenciales
    with open(token_file, "r") as f:
        token_data = json.load(f)
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = Credentials.from_authorized_user_info(token_data, SCOPES)

    service = build("calendar", "v3", credentials=creds)
    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        return {"status": "success", "message": f"Evento {event_id} eliminado correctamente."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def actualizar_evento_google_calendar(
    event_id: str,
    summary: str = None,
    description: str = None,
    start_datetime: str = None,
    end_datetime: str = None,
    token_file: str = "token.json",
    time_zone: str = "America/Lima",
    calendar_id: str = "primary"
):
    """
    Actualiza un evento existente en Google Calendar.
    Solo se modifican los campos que se proporcionan.
    """

    # Cargar credenciales
    with open(token_file, "r") as f:
        token_data = json.load(f)
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = Credentials.from_authorized_user_info(token_data, SCOPES)
    service = build("calendar", "v3", credentials=creds)

    # Obtener evento existente
    try:
        evento = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    except Exception as e:
        return {"status": "error", "message": f"No se pudo encontrar el evento: {e}"}

    # Actualizar los campos si se proporcionan
    if summary:
        evento["summary"] = summary
    if description:
        evento["description"] = description
    if start_datetime:
        evento["start"] = {"dateTime": start_datetime, "timeZone": time_zone}
    if end_datetime:
        evento["end"] = {"dateTime": end_datetime, "timeZone": time_zone}

    # Enviar actualización
    try:
        evento_actualizado = service.events().update(
            calendarId=calendar_id, eventId=event_id, body=evento).execute()
        return {
            "status": "success",
            "message": "Evento actualizado correctamente.",
            "event_id": evento_actualizado.get("id"),
            "htmlLink": evento_actualizado.get("htmlLink"),
            "summary": evento_actualizado.get("summary"),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def listar_eventos_google_calendar(
    token_file="token.json",
    max_resultados=10,
    calendar_id="primary"
):
    """
    Lista los próximos eventos del calendario de Google.
    """
    #SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    # Cargar credenciales
    with open(token_file, "r") as f:
        token_data = json.load(f)

    creds = Credentials.from_authorized_user_info(token_data, SCOPES)
    service = build("calendar", "v3", credentials=creds)

    time_min = datetime.utcnow().isoformat() + "Z"  # ahora
    time_max = (datetime.utcnow() + timedelta(days=7)).isoformat() + "Z"  # 7 días

    eventos_resultado = service.events().list(
        calendarId=calendar_id,
        maxResults=max_resultados,
        singleEvents=True,
        orderBy="startTime",
        timeMin=time_min,
        timeMax=time_max
    ).execute()    
    # Llamar a la API para listar eventos
    #eventos_resultado = service.events().list(
    #    calendarId=calendar_id,
    #    maxResults=max_resultados,
    #    singleEvents=True,
    #    orderBy="startTime"
    #).execute()
    
    eventos = eventos_resultado.get("items", [])

    if not eventos:
        print("No se encontraron eventos.")
        return []

    # Mostrar resultados
    for ev in eventos:
        id = ev.get("id", "Sin Id")
        nombre = ev.get("summary", "Sin título")
        start = ev["start"].get("dateTime", ev["start"].get("date"))
        end = ev["end"].get("dateTime", ev["end"].get("date"))
        print(f"{id} - {nombre}: {start} -> {end}")

    return eventos

def crear_evento_google_calendar(
    summary: str,
    description: str,
    start_datetime: str,
    end_datetime: str,
    token_file: str = "token.json",
    time_zone: str = "America/Lima"
) -> dict:
    """
    Crea un evento en el calendario de Google autenticado con el token OAuth local.
    Fechas deben ir en formato ISO (YYYY-MM-DDTHH:MM:SS).
    """

    # Carga las credenciales desde archivo
    with open(token_file, "r") as f:
        token_data = json.load(f)

    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = Credentials.from_authorized_user_info(token_data, SCOPES)
    service = build("calendar", "v3", credentials=creds)

    event_data = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_datetime, "timeZone": time_zone},
        "end": {"dateTime": end_datetime, "timeZone": time_zone},
    }

    try:
        created_event = service.events().insert(calendarId="primary", body=event_data).execute()
        return {
            "status": "success",
            "event_id": created_event.get("id"),
            "html_link": created_event.get("htmlLink"),
            "message": f"Evento '{summary}' creado.",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }
        
if __name__ == "__main__":
    # Coloca aquí el ID de un evento real
    #my_event_id = "4ptbsusm7oru0u73jfj9klkh7k" # id de eventos

    #resultado = eliminar_evento_google_calendar(event_id=my_event_id)
    #print(resultado)
    
    # Coloca aquí el ID real de un evento de tu calendario
    #my_event_id = "4ptbsusm7oru0u73jfj9klkh7k" # id de eventos

    #resultado = actualizar_evento_google_calendar(
    #    event_id=my_event_id,
    #    summary="VIAJE A HUANCAYO MODIFICADO POR KIKE",
    #)
    #print(resultado)
    
    eventos = listar_eventos_google_calendar(max_resultados=5)    
    
    #resultado = crear_evento_google_calendar(
    #    summary="viaje a huancayo",
    #    description="preparate para ir a cruz del sur.",
    #    start_datetime="2025-04-18T16:00:00",
    #    end_datetime="2025-04-18T16:00:00"
    #)
    #print(resultado)
    