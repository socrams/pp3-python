from flask import Flask, Blueprint, request, jsonify
from carrera import Carrera
from users.user import User
from materia import Materia
from materia_profesor import MateriaProfesor
from carrera_informacion import CarreraInformacion
from datetime import datetime


careers_bp = Blueprint('carrera', __name__)

@careers_bp.route('/', methods=['GET', 'POST', 'PUT'])
def AMGCarreras():
        
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)
    userId=User.getUserIDFromToken(_token)

    if _token_status == True:
        
        if request.method == 'GET':
            carreras=Carrera.getCarreras()
            return jsonify(carreras)
        if request.method == 'POST' or request.method == 'PUT':
            data=request.get_json(force = True)
            carrera=Carrera()
            if request.method == 'PUT':
                carrera.id = data['id']
            carrera.descripcion = data['descripcion']
            carrera.duracion = data['duracion']
            if carrera.id and carrera.id is not None:
                carrera.fecha_modificacion = datetime.now()
                carrera.modificacion_usuario_id = userId
                result = Carrera.updateCarrera(carrera, userId)
            else:
                carrera.fecha_creacion = datetime.now()
                carrera.creacion_usuario_id = userId
                result = Carrera.addCarrera(carrera)
        return jsonify(result), 200
    else:
        return jsonify(_token_status), 401
    

@careers_bp.route('/<idCarrera>', methods=['GET', 'DELETE'])
def DGCarrera(idCarrera):
    
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)
    userId=User.getUserIDFromToken(_token)
        
    if _token_status == True:
        if request.method == 'GET':
            carrera=Carrera.getCarreraById(idCarrera)
            return jsonify(carrera)
        if request.method == 'DELETE':
            result = Carrera.delCarrera(idCarrera)
            return jsonify(result)
    else:
        return jsonify(_token_status), 401

@careers_bp.route('/<idCarrera>/informacion', methods=['GET', 'POST', 'PUT'])
def AMGInformacion(idCarrera):
        
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)
    userId=User.getUserIDFromToken(_token)
        
    if _token_status == True:
        
        if request.method == 'GET':
            informacion=CarreraInformacion.getCarreraInformacion(idCarrera)
            return jsonify(informacion)
        
        if request.method == 'POST' or request.method == 'PUT':
            data=request.get_json(force = True)
            informacion=CarreraInformacion()
            informacion.id = data['id']
            informacion.carrera_id = data['carrera_id']
            informacion.tipo = data['tipo']
            informacion.url = data['url']
            informacion.vigencia = data['vigencia']

            if informacion.id is None:
                result = CarreraInformacion.addInformacion(informacion) 
            else:
                result = CarreraInformacion.updateInformacion(informacion)
            return jsonify(result), 200
    else:
        return jsonify(_token_status), 401
            
@careers_bp.route('/<idCarrera>/informacion/<id>', methods=['GET', 'DELETE'])
def DGCarreraInformacion(idCarrera, id):
     
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)
         
    if _token_status == True:
        if request.method == 'GET':
            informacion=CarreraInformacion.getInformacionById(id)
            return jsonify(informacion)
        if request.method == 'DELETE':
            result = CarreraInformacion.delInformacion(id)
            return jsonify(result)
    else:
        return jsonify(_token_status), 401


@careers_bp.route('/<idCarrera>/materias/', methods=['GET','POST', 'PUT'])
def AMGMateria(idCarrera):
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)
    userId=User.getUserIDFromToken(_token)
         
    if _token_status == True:    
        if request.method == 'GET':
            materias=Materia.getMateria(idCarrera)
            return jsonify(materias)

        if request.method == 'POST' or request.method == 'PUT':
            data=request.get_json(force = True)
            print(data)
            materia=Materia()
            if 'id' in data:
                materia.id = data['id']
            else:
                materia.id = None

            materia.carrera_id = data['carrera_id']
            materia.anio = data['anio']
            materia.descripcion = data['descripcion']
            if 'vigencia' in data:
                materia.vigencia = data['vigencia']

            if materia.id is None:
                result = Materia.addMateria(materia)
                return jsonify(result)
            else:
                result = Materia.updateMateria(materia)
                return jsonify(result)
    else:
        return jsonify(_token_status), 401
    
@careers_bp.route('/<idCarrera>/materias/<id>', methods=['GET','DELETE'])
def BGMateria(idCarrera, id):
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)
    userId=User.getUserIDFromToken(_token)
         
    if _token_status == True:    
        if request.method == 'GET':
            materia=Materia.getMateriaById(id)
            return jsonify(materia)
        
        if request.method == 'DELETE':
            result = Materia.deleteMateria(id)
            return jsonify(result)
    else:
        return jsonify(_token_status), 401
    


@careers_bp.route('/<idCarrera>/materias/<id>/profesor/', methods=['GET','POST', 'PUT'])
def AMGProfesor(idCarrera, id):
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)
    if _token_status == True:    
        if request.method == 'GET':
            profesor=MateriaProfesor().getMateriaProfesor(id)
            return jsonify(profesor)

        if request.method == 'POST' or request.method == 'PUT':
            data=request.get_json(force = True)
            profesor=MateriaProfesor()
            profesor.id = data['id']
            profesor.materia_id = data['materia_id']
            profesor.comision = data['comision']
            profesor.turno = data['turno']
            profesor.profesor = data['profesor']
            profesor.desde = data['desde']
            profesor.hasta = data['hasta']

            if profesor.id is None:
                result = MateriaProfesor.addProfesor(profesor)
                return jsonify(result)
            else:
                result = MateriaProfesor.updateProfesor(profesor)
                return jsonify(result)
    else:
        return jsonify(_token_status), 401
    
@careers_bp.route('/<idCarrera>/materias/<idMateria>/profesor/<id>', methods=['GET','DELETE'])
def BGProfesor(idCarrera, idMateria, id):
    _token = request.headers.get('Authorization')
    _token_status = User.validateToken(_token)
         
    if _token_status == True:    
        if request.method == 'GET':
            materia=MateriaProfesor.getMateriaProfesorById(id)
            return jsonify(materia)
        
        if request.method == 'DELETE':
            result = MateriaProfesor.deleteProfesor(id)
            return jsonify(result)
    else:
        return jsonify(_token_status), 401