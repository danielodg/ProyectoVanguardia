from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import google.cloud.dialogflowcx_v3beta1 as dialogflow
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Configurar Dialogflow CX
PROJECT_ID = "proyectovanguardia"
AGENT_ID = "14ad30b3-ec14-44b6-8a0c-25f3bfe6302e"
LOCATION = "global"
SESSION_ID = "12345"
LANGUAGE_CODE = "es"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

# Inicializar cliente de Dialogflow CX
client = dialogflow.SessionsClient()
session_path = client.session_path(PROJECT_ID, LOCATION, AGENT_ID, SESSION_ID)

def detect_intent_texts(text):
    query_input = dialogflow.QueryInput(
        text=dialogflow.TextInput(text=text),
        language_code=LANGUAGE_CODE
    )
    request = dialogflow.DetectIntentRequest(session=session_path, query_input=query_input)
    response = client.detect_intent(request=request)
    
    if response.query_result.response_messages:
        return response.query_result.response_messages[0].text.text[0]
    else:
        return "Lo siento, no entendí tu mensaje."

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    user_message = data['message']
    bot_response = detect_intent_texts(user_message)
    emit('response', {'message': bot_response})

if __name__ == '__main__':
    socketio.run(app, debug=True)
