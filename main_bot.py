import re
import random
import sys
sys.path.append('c:\python310\lib\site-packages')

from json import JSONEncoder

from flask import Flask,request, jsonify
from flask_cors import CORS


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/chat_server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = 'USERS'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(255), default = '')
    email = db.Column(db.String(255), default = '')
    full_name = db.Column(db.String(255), default = '')
    phone = db.Column(db.String(255), default = '')
    enabled = db.Column(db.Boolean, default = True)
    status = db.Column(db.Boolean, default = True)
    creation_date = db.Column(db.DateTime)
    creation_user_id = db.Column(db.Integer)
    last_update = db.Column(db.DateTime)
    last_update_user_id = db.Column(db.Integer)
    last_reset_password = db.Column(db.DateTime)
    should_reset_password = db.Column(db.Boolean)

    def __init__(self, name, password, email, full_name, phone, enabled, status, creation_date, creation_user_id, last_update,
                last_update_user_id, should_reset_password,
                last_reset_password) -> None:
        super().__init__()
        self.name = name
        self.password = password
        self.email = email
        self.full_name = full_name
        self.phone = phone
        self.enabled = enabled
        self.status = status
        self.creation_date = creation_date
        self.creation_user_id = creation_user_id
        self.should_reset_password = should_reset_password
        self.last_update = last_update
        self.last_update_user_id = last_update_user_id
        self.last_reset_password = last_reset_password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'password', 'email', 'full_name', 'phone', 'enabled', 'status', 'creation_date', 
                'creation_user_id', 'last_update', 'last_update_user_id', 'last_reset_password', 'should_reset_password')


#Creamos el almacenamiento mono usuario
user_schema = UserSchema()
#Creamos el almacenamiento multiusuario
users_schema = UserSchema(many=True)


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
    response = ['puedes decirlo con otras palabras, no entendi', 'no estoy seguro de lo que quieres', 'intenta con otras palabras'][random.randrange(3)]
    return response

######################## Obtener usuarios ################################
@app.route('/users/', methods=['GET'])
def users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/users/<id>', methods=['GET'])
def userById(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@app.route('/users/', methods=['POST'])
def addUser():
    name = request.json['name']
    password = request.json['password']
    phone = request.json['phone']
    email = request.json['email']
    full_name = request.json['full_name']

    nUser = User(name, password, email, full_name, phone, True, True, datetime.now(), 0, datetime.now(), 0, True, datetime.now())

    db.session.add(nUser)
    db.session.commit()
    return user_schema.jsonify(nUser)

@app.route('/users/', methods=['PUT'])
def putUser():

    data = request.get_json(force = True)
    id = data['id']
    change = False

    oldUser = User.query.get(id)

    name = data['name']
    password = data['password']
    phone = data['phone']
    email = data['email']
    full_name = data['full_name']
    enabled = data['enabled']
    status = data['status']

    if oldUser.name != name:
        change = True
        oldUser.name = name
    
    if oldUser.password  != password:
        change = True
        oldUser.password = password


    if oldUser.phone != phone:
        change = True
        oldUser.phone = phone

    if oldUser.email != email:
        change = True
        oldUser.email = email

    if oldUser.full_name != full_name:
        change = True
        oldUser.full_name = full_name

    if oldUser.enabled != enabled:
        change = True
        oldUser.enabled = enabled

    if oldUser.status != status:
        change = True
        oldUser.status = status

    if change:
        db.session.commit()
        return jsonify("{'result': 'Updateado'}")
    else:
        return jsonify("{'result': 'Sin cambios'}")
    

@app.route('/users/<id>', methods=['DELETE'])
def delUser(id):

    nUser = User.query.get(id)

    nUser.status = False
    nUser.last_update = datetime.now()
    nUser.enabled = False
    
    ##try:
    db.session.commit()
    return jsonify("{'result': 'Eliminado'}")
    #catch:
    #    return jsonify("{'result': 'Error'}")
    #end

######################## Obtener usuarios ################################


######################## Chat manager ################################
@app.route('/chat/<message>', methods=['GET'])
def index(message):
    ahora = datetime.now()
    hora_actual = ahora.strftime("%H:%M %p")
    return jsonify({ 'id':'server', 'respuesta': get_response(message),'hora':hora_actual})




if __name__=="__main__":
    app.run(debug=True)

