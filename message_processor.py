import re
import random

from response import Response

class MessageProcessor:
    
    def __init__(self, responses) -> None:
        self.responses=responses

    def get_response(self, user_input):
        split_message = re.split(r'\s|[,:;.?!-_]\s*', str(user_input).lower())
        _response = self.check_all_message(split_message)
        return _response

    def message_probability(self, user_message, recognized_words, single_response=False, required_word=[]):
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
            else:
                print('es igual')

        if has_required_words or single_response:
            return int(percentage * 100)
        else:
            return 0

    def check_all_message(self, message):
        highest_prob = {}

        def botresponse(bot_response, list_of_words, single_response = False, required_words=[]):
            nonlocal highest_prob
            highest_prob[bot_response] = self.message_probability(message, list_of_words, single_response, required_words)

        for r in self.responses:
            botresponse(r.response, re.split(r'\s|[,:;.?!-_]\s*', str(r.answer).lower()), r.moreQuestion, re.split(r'\s|[,:;.?!-_]\s*', str(r.answer).lower()))

        best_match = max(highest_prob, key=highest_prob.get)
        print(highest_prob)

        return self.unknown() if highest_prob[best_match] < 20 else best_match

    def unknown(self):
        response = ["'Puedes decirlo con otras palabras? No estoy comprendiendo lo que necesitas. Si quieres ayuda, puedes enviar Menu para brindarte opciones.'", 'No estoy seguro de lo que quieres. Si quieres ayuda, puedes enviar Menu para brindarte opciones.', 'Intenta con otras palabras. Si quieres ayuda, puedes enviar Menu para brindarte opciones.'][random.randrange(3)]
        return response