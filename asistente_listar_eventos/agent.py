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
    max_resultados: str = Field(description="Numero maximos de eventos a listar, en caso NO IDENTIFIQUE el numero por defecto coloca el valor de 10, si el dato obtenido del contenido del usuario SOBREPASA el valor de 10, coloca el valor 10")

def listar_eventos_google_calendar(max_resultados: str) -> dict:
    eventos = fc.listar_eventos_google_calendar(
        max_resultados=max_resultados
    )
    
    list_eventos = []
    for ev in eventos:
        id = ev.get("id", "Sin Id")
        nombre = ev.get("summary", "Sin título")
        start = ev["start"].get("dateTime", ev["start"].get("date"))
        end = ev["end"].get("dateTime", ev["end"].get("date"))
        list_eventos.append(
            {
                "id":id,
                "nombre":nombre,
                "start":start,
                "end":end,
            }
        )

    return list_eventos
    
root_agent = Agent(
    name="asistente_lista_eventos_google_calendar",
    #model="gemini-2.0-flash",
    model=LiteLlm(model="openai/gpt-4o"), # LiteLLM model string format
    description=(
        "Agente para listar los eventos que se encuentran registrados en google calendar."
    ),
    instruction=(
    f"""
    En base al contenido brindado por el usuario, genera un formato JSON como:
     {json.dumps(CreateCalendarInfoInput.model_json_schema(), indent=2)}.
    
    ONLY con el formato JSON obtenido utiliza la tool 'create_calendar_event'.
    
    Con el resultado obtenido de la tool, genera una lista adecuada con todos los valores para devolver al usuario
    """
    ),
    tools=[listar_eventos_google_calendar],
)