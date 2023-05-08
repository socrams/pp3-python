from json import JSONEncoder

from flask import Flask,request, jsonify
from flask_cors import CORS

from datetime import datetime

from user import User
from connection import Connection
from response import Response
from config import LANGUAJE
from message_processor import MessageProcessor

import enchant

app = Flask(__name__)
CORS(app)


#interpreter=enchant.Dict(LANGUAJE)

######################## Obtener usuarios ################################
@app.route('/users/', methods=['GET'])
def users():
    #all_users = User.query.all()
    #filterResult = []
    #for _user in all_users:
    #    if _user.status:
    #        filterResult.append(_user)
    #result = users_schema.dump(filterResult)
    #return jsonify(result)
    alluser=User.getUsers()
    return jsonify(alluser)

@app.route('/users/<id>', methods=['GET'])
def userById(id):
    user = User.getUserById(id)
    return jsonify(user)

@app.route('/users/', methods=['POST'])
def addUser():
    name = request.json['name']
    password = request.json['password']
    phone = request.json['phone']
    email = request.json['email']
    full_name = request.json['full_name']

    nUser = User(name, password, email, full_name, phone, True, True, datetime.now(), 0, datetime.now(), 0, True, datetime.now())

    #db.session.add(nUser)
    #db.session.commit()
    return "" #user_schema.jsonify(nUser)

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
        #db.session.commit()
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
    #db.session.commit()
    return jsonify("{'result': 'Eliminado'}")
    #catch:
    #    return jsonify("{'result': 'Error'}")
    #end

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

