from flask import Flask, request, jsonify
import os
import openai

# Inicializar la aplicación Flask
app = Flask(__name__)



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