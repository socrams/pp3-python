import re
import random

from response import Response

class MessageProcessor:
    
    def __init__(self) -> None:

        self.responses=[
            
            #response(id, pregunta, respuesta, opciones, más preguntas, más opciones)
            Response(1, "hola", "¡Hola! \n¿En qué puedo ayudarte?", "", False, False),
            Response(2, "buenos dias", "¡Buen día! \n¿En qué puedo ayudarte?", "", False, False),
            Response(3, "menu","Los menús disponibles son: \n - Información de carreras \n - Documentación necesaria para la inscripción \n - Fechas de parciales \n - Fechas de finales \n - Pedidos de constancias de alumno regular. ¿En qué tema te gustaría profundizar?", "Información de carreras, Documentación necesaria para la inscripción, Fechas de parciales, Fechas de finales, Pedidos de constancias de alumno regular", True, False),
            Response(4, "informacion de carreras", "Las carreras que dictamos son: \n - Técnico Superior en Análisis de Sistemas \n - Enfermería \n - Seguridad e Higiene. \n ¿En qué carrera te gustaría más información?", "Técnico Superior en Análisis de Sistemas, Enfermería, Seguridad e Higiene", True, False),
            Response(5, "tecnicatura en sistemas", "La Tecnicatura Superior en Análisis de Sistemas consta de 3 años de duración.\n Tiene como objetivo formar profesionales capaces de analizar, diseñar, desarrollar, implementar y mantener sistemas de información. \n¿En qué turno te gustaría cursar (mañana, tarde, noche)?", "Mañana, Tarde, Noche", True, False),
            Response(6, "enfermeria", "La carrera de Enfermería tiene una duración de 3 años y tiene como objetivo formar profesionales capaces de brindar cuidados integrales a personas, familias y comunidades en diferentes niveles de atención de salud. ¿En qué turno te gustaría cursar (mañana, tarde, noche)?", "Mañana, Tarde, Noche", True, False),
            Response(7, "seguridad e higiene", "La carrera de Seguridad e Higiene tiene una duración de 3 años y tiene como objetivo formar profesionales capaces de planificar, implementar y dirigir programas de prevención y control de riesgos en el ámbito laboral y ambiental. ¿En qué turno te gustaría cursar (mañana, tarde, noche)?", "Mañana, Tarde, Noche", True, False),
            ]


    def get_response(self, user_input):
        split_message = re.split(r'\s|[,:;.?!-_]\s*', str(user_input).lower())
        response = self.check_all_message(split_message)
        return response

    def message_probability(self, user_message, recognized_words, single_response=False, required_word=[]):
        message_certainty = 0
        has_required_words = True

        for word in user_message:
            print(word)
            if word in recognized_words:
                print(word)
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

    def check_all_message(self, message):
        highest_prob = {}

        def response(bot_response, list_of_words, single_response = False, required_words=[]):
            nonlocal highest_prob
            highest_prob[bot_response] = self.message_probability(message, list_of_words, single_response, required_words)

        for Response in self.responses:
            response(Response.response, Response.answer, Response.moreQuestion, re.split(r'\s|[,:;.?!-_]\s*', str(Response.answer).lower()))

        best_match = max(highest_prob, key=highest_prob.get)
        print(highest_prob)

        return self.unknown() if highest_prob[best_match] < 1 else best_match

    def unknown(self):
        response = ["'puedes decirlo con otras palabras, no entendi'", 'no estoy seguro de lo que quieres', 'intenta con otras palabras'][random.randrange(3)]
        return response