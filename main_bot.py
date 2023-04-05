import re
import random
from flask import Flask,jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_response(user_input):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
    response = check_all_message(split_message)
    return response


def message_probability(user_message, recognized_words, single_response=False, required_word=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognized_words:
            message_certainty+=1

    percentage = float(message_certainty) / float (len(recognized_words))

    for word in required_word:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_message(message):
    highest_prob = {}

    def response(bot_response, list_of_words, single_response = False, required_words=[]):
        nonlocal highest_prob
        highest_prob[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hola', ['hola', 'klk', 'buenas', 'ola'], single_response = True)
    
    response('Estoy bien y vos?', ['como', 'estas','va', 'vas', 'tas'], required_words = ['como']) 

    response('Gracias', ['gracias', 'agradezco', 'bien', 'de nada'], required_words = ['gracias'])

    best_match = max(highest_prob, key=highest_prob.get)
    print(highest_prob)

    return unknown() if highest_prob[best_match] < 1 else best_match

def unknown():
    response = ["'puedes decirlo con otras palabras, no entendi'", 'no estoy seguro de lo que quieres', 'intenta con otras palabras'][random.randrange(3)]
    return response



@app.route('/<message>', methods=['GET'])
def index(message):
    ahora = datetime.now()
    hora_actual = ahora.strftime("%H:%M %p")
    return jsonify({ 'id':'server', 'respuesta': get_response(message),'hora':hora_actual})

if __name__=="__main__":
    app.run(debug=True)

