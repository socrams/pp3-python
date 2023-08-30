from flask import BluePrint, request, jsonify
from responses.response import Response
from message_processor import MessageProcessor
from datetime import datetime
import random

chats_bp=BluePrint('chat', __name__)

@chats_bp.route('/chat/<message>', methods=['GET'])
def index(message):
    ahora = datetime.now()
    hora_actual = ahora.strftime("%H:%M %p")
    responses=Response.getResponseLocal()
    finalMessage = message
    mp=MessageProcessor(responses)
    response=mp.get_response(finalMessage)
    return jsonify({ 'id':'server', 'respuesta': getObject(response, responses),'hora':hora_actual})


def getObject(message, responses):
    for r in responses:
        if (r.response == message):
            print(r.to_dict())
            return r.to_dict()

    error_response = Response()
    error_response.answer = "Palabra no encontrada"
    error_response.id = -1
    error_response.response = ['Puedes decirlo con otras palabras? No estoy comprendiendo lo que necesitas. Si quieres ayuda, puedes enviar Menu para brindarte opciones.', 'No estoy seguro de lo que quieres. Si quieres ayuda, puedes enviar Menu para brindarte opciones.', 'Intenta con otras palabras. Si quieres ayuda, puedes enviar Menu para brindarte opciones.'][random.randrange(3)]
    error_response.options = "Menu, informacion de carreras"
    error_response.moreOptions = True
    error_response.moreQuestion = False

    return error_response.to_dict()