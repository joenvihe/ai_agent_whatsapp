from datetime import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from asistente_utils import func_calendario_google as fc
from pydantic import BaseModel, Field
import json # Needed for pretty printing dicts

fecha_formateada = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
#2025-04-18T16:00:00
# Input schema ONLY for the agent
class CreateCalendarInfoInput(BaseModel):
    summary: str = Field(description="Titulo del evento, es un resumen del contenido brindado por el usuario")
    description: str = Field(description="Descripcion general del evento, debe ser igual al contenido brindado por el usuario.")
    start_datetime: str = Field(description=f"Fecha, hora y minutos de inicio del evento, se debe obtener del contenido enviado por el usuario.La fecha identificada es OBLIGATORIO CONVERTIRLO al formato ISO estándar: yyyy-mm-ddThh:mm:ss, si no encuentras la fecha y hora o se encuentra INCOMPLETO en el texto COMPLETA con los datos del dia de hoy {fecha_formateada}")
    end_datetime: str = Field(description="Fecha, hora y minutos de fin del evento, se debe obtener del contenido enviado por el usuario.La fecha identificada es OBLIGATORIO CONVERTIRLO al formato ISO estándar: yyyy-mm-ddThh:mm:ss, si no encuentras la fecha y hora o se encuentra INCOMPLETO en el texto COMPLETA con los datos de la fecha inicio")


def create_calendar_event(summary: str,description: str,start_datetime: str,end_datetime: str) -> dict:
    resultado = fc.crear_evento_google_calendar(
        summary=summary,
        description=description,
        start_datetime=start_datetime,
        end_datetime=end_datetime
    )
    
root_agent = Agent(
    name="asistente_agenda_google_calendar",
    #model="gemini-2.0-flash",
    model=LiteLlm(model="openai/gpt-4o"), # LiteLLM model string format
    description=(
        "Agente para poder registrar eventos en el google calendar."
    ),
    instruction=(
    f"""
    En base al contenido brindado por el usuario, genera un formato JSON como:
     {json.dumps(CreateCalendarInfoInput.model_json_schema(), indent=2)}.
    
    ONLY con el formato JSON obtenido utiliza la tool 'create_calendar_event' 
    para crear un evento en el calendario de google
    """
    ),
    tools=[create_calendar_event],
)