from flask import Flask, request, jsonify
import os
import openai
from datetime import datetime
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path

# Autenticación con Google
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        except Exception as e:
            print(e)
    return creds

def create_calendar_event(evento):
    service = build('calendar', 'v3', credentials=authenticate_google())

    # Datos del evento
    event = {
        'summary': evento["titulo"],  # Título
        'location': evento["lugar"],  # Ubicación
        'description': evento["descripcion"],  # Descripción
        'start': {
            'dateTime': evento["fecha_inicio"],  # Fecha y hora de inicio
            'timeZone': 'America/Lima',  # Zona horaria
        },
        'end': {
            'dateTime': evento["fecha_fin"],  # Fecha y hora de fin
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
    return 'Evento creado:{}'.format(event_result['htmlLink'])



# Inicializar la aplicación Flask
app = Flask(__name__)

@app.route('/cal', methods=['POST'])
def add_google_calendar():
    extracted_text = ""
    etapa = ""
    try:
        # Llamar al modelo para procesar el prompt y extraer entidades
        openai.api_key = os.getenv("OPENAI_API_KEY")
        client = openai.OpenAI()  # Create an OpenAI client
        data = request.get_json()
        prompt = data.get("question", "")

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
                        - Si no encuentras la fecha de fin asume la fecha actual de hoy.
                        - Si no se menciona una ubicación, el valor en el JSON debe ser null.
                        - Asegúrate de ser preciso en la interpretación del texto.

                    Ejemplo de entrada:
                        Texto: cita en el colegio de amelie el martes 30 de marzo del 2025, a las 9 am        
                    Salida esperada:
                        
                            'titulo': 'Cita en el colegio de Amelie',
                            'descripcion": 'Cita programada en el colegio de Amelie para el martes 30 de marzo del 2025 a las 9:00 am.',
                            'lugar': 'colegio de Amelie',
                            'fecha_inicio': '2025-03-30T09:00:00',
                            'fecha_fin': '2025-03-30T09:00:00'
                        
                    """}
            ]
        )
        etapa = "1"

        # Obtener el contenido de la respuesta del modelo
        extracted_text = response.choices[0].message.content.strip()
        
        # Convertir la salida en formato JSON
        try:
            etapa = "2"
            print(extracted_text)
            entities_json = json.loads(extracted_text)
            etapa = "3"
            respuesta = create_calendar_event(entities_json)
            etapa = "4"
            entities_json = {"respuesta:":"exito: {}  texto: {}".format(respuesta,extracted_text)}
            etapa = "5"
            
        except json.JSONDecodeError:
            etapa = "6"
            entities_json = {"respuesta": "No se pudo decodificar la respuesta como JSON. {}".format(respuesta,extracted_text)}
                
        return jsonify({"answer": entities_json["respuesta"]})
    except Exception as e:
        return jsonify({"answer": "error_cambio :{}  texto:{} etapa:{}".format(str(e),extracted_text,etapa)}), 500


@app.route('/ask', methods=['POST'])
def ask_openai():
    try:
        # Obtener la pregunta desde el cuerpo de la solicitud
        openai.api_key = os.getenv("OPENAI_API_KEY")
        client = openai.OpenAI()  # Create an OpenAI client
        data = request.get_json()
        question = data.get("question", "")

        # Llamar al modelo de OpenAI
        # response = openai.ChatCompletion.create(
        response = client.chat.completions.create(
            #model="text-davinci-003",  # Puedes ajustar el modelo según sea necesario
            #prompt=question,
            #max_tokens=100
            model="gpt-3.5-turbo",  # Utiliza el modelo más reciente
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": question}
            ]
        )

        # Responder con el resultado
        # return jsonify({"answer": response.choices[0].text.strip()})
        #answer = response['choices'][0]['message']['content']
        answer = response.choices[0].message.content
        return jsonify({"answer": answer.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)