from flask import Blueprint, request, jsonify

from flask_cors import CORS
from users.user import User

auth_bp = Blueprint('auth', __name__)
CORS()


@auth_bp.route('/login', methods=['OPTIONS'])
def handle_options():
    return '', 200

@auth_bp.route('/login/', methods=['POST'])
def login():
    try:
        credentials = request.get_json()
        _mail = credentials['mail']
        _pass = credentials['password']
        _user = User.login(_mail, _pass)
        _token = User.generar_token(_user.id)
        
        User.setLastLogin(_user.id)
        return jsonify({'message': _token})

    except Exception as e:
        print('Error al desencriptar. Detalle', e)
        return jsonify({'message': 'ERROR'})    

@auth_bp.route('/validateToken/',methods=['GET', 'POST'])
def validateToken():
    if request.method == 'GET':
        _token = request.headers.get('Authorization')
        _token_status = User.validateToken(_token)
        return (_token_status == True), 200
    elif request.method == 'POST':
        _token = request.headers.get('Authorization')
        print(_token)
        _token_status = User.validateToken(_token)
        print(_token_status)
        return jsonify(_token_status == True), 200
