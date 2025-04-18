import openai
import json
import os
from datetime import datetime

# Configura tu clave API de OpenAI


def extract_entities(prompt):
    # Llamar al modelo para procesar el prompt y extraer entidades
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI()  # Create an OpenAI client

    # Obtener la fecha actual y formatearla
    fecha_formateada = datetime.now().strftime("%d/%m/%Y")
    print("La fecha de hoy es:", fecha_formateada)


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Utiliza el modelo más reciente
        messages=[
            {"role": "system", "content": "Eres un asistente que extrae entidades de texto y las formatea en un JSON."},
            {"role": "user", "content": f"""
                Recuerda que la fecha de hoy es {fecha_formateada}.

                Tu tarea consiste en analizar el siguiente texto: '{prompt}', y extraer las siguientes entidades para crear un JSON estructurado:

                - titulo: Proporciona un título claro y representativo del contenido del texto.
                - descripcion: Elabora una descripción completa y adecuada basada en el texto, incluyendo detalles importantes.
                - lugar: Identifica y extrae cualquier ubicación o lugar mencionado en el texto, si existe.
                - fecha_inicio: Si en el texto se encuentra una fecha o período de inicio, conviértelo al formato ISO estándar: yyyy-mm-ddTHH:MM:SSZ., si no encuentras la fecha en el texto coloca la del dia de hoy
                - fecha_fin: Si el texto incluye una fecha o período de finalización, conviértelo también al formato ISO: yyyy-mm-ddTHH:MM:SSZ.

                Nota: 
                    - El resultado debe estar formateado como un único JSON válido.
                    - Si no encuentras la fecha de inicio asume la fecha actual de hoy.
                    - Si no se menciona una ubicación o fecha de fin, el valor en el JSON debe ser null.
                    - Asegúrate de ser preciso en la interpretación del texto.

                Ejemplo de entrada:
                    Texto: cita en el colegio de amelie el martes 30 de marzo del 2025, a las 9 am        
                Salida esperada:
                    
                        'titulo': 'Cita en el colegio de Amelie',
                        'descripcion": 'Cita programada en el colegio de Amelie para el martes 30 de marzo del 2025 a las 9:00 am.',
                        'lugar': 'colegio de Amelie',
                        'fecha_inicio': '2025-03-30T09:00:00',
                        'fecha_fin': null
                    
                """}
        ]
    )

    # Obtener el contenido de la respuesta del modelo
    extracted_text = response.choices[0].message.content.strip()
    
    # Convertir la salida en formato JSON
    try:
        print(extracted_text)
        entities_json = json.loads(extracted_text)
    except json.JSONDecodeError:
        entities_json = {"error": "No se pudo decodificar la respuesta como JSON."}
    
    return entities_json

# Ejemplo de uso
prompt_list = [
    "cita en el colegio de amelie el martes 30 de marzo del 2025, a las 9 am",
    "salida con nohe el martes al cine",
    "llevar la maraca e ir a la casa de papa el dia de mañana",
    "recuerdame tomar mi medicina todas las tardes hasta mayo",
    "registra cita para amelie por 1 semana desde hoy",
    "registra cita para amelie durante el perido de una semana a partir de hoy",
    """
    comprar platano, manzana hoy por la noche a las 8 pm
    """,
    "Remind me to take vitamin D3 every afternoon until March",
    "Get child-friendly events in Dublin new years week, add to family calendar",
    "Find my grocery list and send my husband a reminder about it in 2 hours",
    "Find the next sunny day in SF and add beach day to calendar",
    "Add client lunch to the next available free slot on my calendar",
    "I found a house, remove ALL upcoming house tour events",
]
prompt = "Jorge Enrique tiene 17 años"
result = extract_entities(prompt_list[2])

print(result)
