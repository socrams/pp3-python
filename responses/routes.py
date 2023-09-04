from flask import Blueprint, request, jsonify
from responses.response import Response
from users.user import User

response_bp = Blueprint('response', __name__)

@response_bp.route('/', methods=['GET'])
def response():
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)
    if _token_status == True:
        responses=Response.getResponses()
        return jsonify(responses)
    else:
        return jsonify(_token_status), 401

@response_bp.route('/<id>', methods=['PUT', 'DELETE', 'UPDATE'])    
def putResponse(id):
    if request.method == 'PUT' or request.method == 'UPDATE':
        data = request.get_json(force = True)
        id = data['id']
        answer = data['answer']
        response= data['response']
        options = data['options']
        moreOptions = data['moreoptions']
        moreQuestion = data['morequestion']
        otro_response=Response()
        otro_response.id = id
        otro_response.answer= answer
        otro_response.response=response
        otro_response.options=options
        otro_response.morequestion=moreQuestion
        otro_response.moreoptions=moreOptions
        result = Response.updateResponse(otro_response)
    else:
        result = Response.delResponse(id)

    return jsonify(result)

@response_bp.route('/', methods=['POST'])
def postResponse():
    data = request.get_json(force = True)
    id = data['id']
    answer = data['answer']
    response= data['response']
    options = data['options']
    moreOptions = data['moreOptions']
    moreQuestion = data['moreQuestion']
    response = data['response']
    otro_response=Response()
    otro_response.id = id
    otro_response.answer= answer
    otro_response.response=response
    otro_response.options=options
    otro_response.moreQuestion=moreQuestion
    otro_response.moreOptions=moreOptions
    result = Response.updateResponse(otro_response)
    return jsonify(result)