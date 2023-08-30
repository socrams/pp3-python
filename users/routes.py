from flask import Blueprint, request, jsonify
from user import User
from datetime import datetime

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
def users():
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)
    if _token_status == True:
        alluser=User.getUsers()
        return jsonify(alluser)
    else:
        return jsonify(_token_status), 401
    
@user_bp.route('/<id>', methods=['GET'])
def userById(id):
    user = User.getUserById(id)
    return jsonify(user)

@user_bp.route('/', methods=['POST'])
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

@user_bp.route('/', methods=['PUT'])
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
        print(password)
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
    
    

@user_bp.route('/<id>', methods=['DELETE'])
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