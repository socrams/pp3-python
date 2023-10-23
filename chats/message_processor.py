import re

from responses.response import Response

class MessageProcessor:
    
    def __init__(self, responses) -> None:
        self.responses=responses

    def get_response(self, user_input):
        split_message = re.split(r'\s|[,:;.?!-_]\s*', str(user_input).lower())
        print(split_message)
        _response = self.check_all_message(split_message)
        return _response

    def message_probability(self, user_message, recognized_words, single_response=False, required_word=[]):
        message_certainty = 0
        has_required_words = True

        #print(user_message)
        #print(recognized_words)
        #print(single_response)
        #print(required_word)
        print("---------------------------")

        for word in user_message:
            if word in recognized_words:
                print("encontre: " + word)
                message_certainty+=1

        # Calcular la probabilidad basada en el número total de palabras en el mensaje del usuario
        if user_message:
            percentage = float(message_certainty) / len(user_message) * 100
        else:
            percentage = 0

        #print(" ".format(user_message))
        #print("Reconocidas: ".format(float (len(recognized_words))))
        #print("encontrada: ".format(float(message_certainty)))
        #percentage = float(message_certainty) / float (len(recognized_words))
        #print(percentage)
        for word in required_word:
            if word not in user_message:
                has_required_words = False
                break

        if has_required_words or single_response:
            return int(percentage)
        else:
            return 0
        
        #if has_required_words or single_response:
        #return int(percentage * 100)
        #else:
        #    return 0

    def check_all_message(self, message):
        highest_prob = {}

        def botresponse(bot_response, list_of_words, single_response = False, required_words=[]):
            nonlocal highest_prob
            highest_prob[bot_response] = self.message_probability(message, list_of_words, single_response, required_words)

        for r in self.responses:
            botresponse(r.response, re.split(r'\s|[,:;.?!-_]\s*', str(r.answer).lower()), r.morequestion, re.split(r'\s|[,:;.?!-_]\s*', str(r.answer).lower()))

        best_match = max(highest_prob, key=highest_prob.get)
        print(highest_prob[best_match])

        return self.unknown() if highest_prob[best_match] < 1 else best_match

    def unknown(self):
        response = ["ERROR"]
        return response
