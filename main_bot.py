from json import JSONEncoder

from flask import Flask,request, jsonify
from flask_cors import CORS

from datetime import datetime

from user import User
from connection import Connection
from response import Response
from config import LANGUAJE, SIGNATURE_KEY
from message_processor import MessageProcessor
from cryptography.fernet import Fernet

# import enchant

app = Flask(__name__)
CORS(app)


#interpreter=enchant.Dict(LANGUAJE)

######################## Obtener usuarios ################################
@app.route('/validateToken/', methods=['GET'])
def validateToken():
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)
    if _token_status == True:
        return jsonify({'message': 'token valido'})
    else:
        return jsonify(_token_status), 401
    
@app.route('/users/', methods=['GET'])
def users():
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)
    if _token_status == True:
        alluser=User.getUsers()
        return jsonify(alluser)
    else:
        return jsonify(_token_status), 401
    
@app.route('/users/<id>', methods=['GET'])
def userById(id):
    user = User.getUserById(id)
    return jsonify(user)

@app.route('/users/', methods=['POST'])
def addUser():
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)

    if (_token_status) == True:
        name = request.json['name']
        password = request.json['password']
        phone = request.json['phone']
        email = request.json['email']
        full_name = request.json['full_name']

        nUser = User()
        nUser.name=name
        nUser.password=password
        nUser.email=email
        nUser.full_name=full_name
        nUser.phone=phone
        nUser.enabled=True
        nUser.status=True
        nUser.should_reset_password=True
        nUser.creation_date=datetime.now()
        nUser.creation_user_id=0
        nUser.last_update=datetime.now()

        userId=User.getUserIDFromToken(_token)
        if userId:
            nUser.last_update_user=userId

        User.addUser(nUser);
        return jsonify({'message': 'usuario creado correctamente'})
    else:
        return jsonify(_token_status), 401
    

@app.route('/users/', methods=['PUT'])
def putUser():
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)

    if (_token_status) == True:
    
        data = request.get_json(force = True)
        id = data['id']
        name = data['name']
        password = data['password']
        phone = data['phone']
        email = data['email']
        full_name = data['full_name']
        enabled = data['enabled']
        status = data['status']

        user=User()
        user.id = id
        user.name= name
        user.email=email
        user.enabled=enabled
        user.full_name=full_name
        user.password=password
        user.phone=phone
        user.status=status

        result = User.updateUser(user)
        return jsonify(result)
    else:
        return jsonify(_token_status), 401
    
    

@app.route('/users/<id>', methods=['DELETE'])
def delUser(id):
    
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)
    if (_token_status) == True:
        nUserId = User.getUserIDFromToken(_token)
        if User.deleteUser(id, nUserId):
            return ({'message': 'Usuario eliminado correctamente.'})
        else:
            return ({'message': 'Usuario no eliminado.'})
    else:
        return jsonify(_token_status), 401


@app.route('/login', methods=['POST'])
def login():
    try:
        #cipher_suite=Fernet(SIGNATURE_KEY)
        #print(request.form['mail'])
        #_mail = cipher_suite.decrypt(request.form['mail'])
        #_pass = cipher_suite.decrypt(request.form['password'])
        # print ("hola")
        credentials = request.get_json()
        _mail = credentials['mail']
        _pass = credentials['password']
        # print(_mail)
        _user = User.login(_mail, _pass)
        _token = User.generar_token(_user.id)
        
        User.setLastLogin(_user.id)
        return jsonify({'message': _token})

    except Exception as e:
        print('Error al desencriptar. Detalle', e)
        return jsonify({'message': 'ERROR'})    
    
######################## Obtener usuarios ################################


######################## Chat manager ################################
@app.route('/chat/<message>', methods=['GET'])
def index(message):
    #ahora = datetime.now()
    #hora_actual = ahora.strftime("%H:%M %p")
    #return jsonify({ 'id':'server', 'respuesta': get_response(message),'hora':hora_actual})
    ahora = datetime.now()
    hora_actual = ahora.strftime("%H:%M %p")
    #print('Interpretada: ' + interpreter.suggest(message)[0])
    
    finalMessage = message #interpreter.suggest(message)
    mp=MessageProcessor()
    return jsonify({ 'id':'server', 'respuesta': mp.get_response(finalMessage),'hora':hora_actual})

if __name__=="__main__":
    app.run(debug=True)

