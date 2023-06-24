from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, DATE, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from connection import Connection
from config import SIGNATURE_KEY
Base=declarative_base()

class Carrera(Base):
    __tablename__= 'CARRERAS'

    id = Column(Integer, primary_key=True)
    descripcion = Column(String(255))
    duracion = Column(Integer)
    fecha_creacion = Column(TIMESTAMP)
    creacion_usuario_id = Column(Integer)
    fecha_modificacion = Column(DATE)
    modificacion_usuario_id = Column(Integer)
    
   
    @staticmethod
    def getCarreras():
        conn=Connection()
        session=conn.getSession()
        carreras=session.query(Carrera).all()
        session.close()
        conn.closeConnection()
        return [c.to_dict() for c in carreras]

    @staticmethod
    def getCarreraById(id):
        conn=Connection()
        session=conn.getSession()
        carrera=session.query(Carrera).filter(Carrera.id == id).first()
        session.close()
        conn.closeConnection()
        return carrera.to_dict()
    
    @staticmethod
    def addCarrera(carrera):
        conn=Connection()
        session=conn.getSession()
        try:
            session.add(carrera)
            session.commit()
            return {'message':'Carrera agregada correctamente'}
        except SQLAlchemyError as e:
            return {'message':'Error al intentar persistir la carrera'}
        finally:
            session.close()
            conn.closeConnection();
    
    @staticmethod
    def delCarrera(id):
        conn=Connection()
        session=conn.getSession()
        session.delete(Carrera.id == id)
        session.commit()
        return {'message':'Se elimino la carrera.'}

    @staticmethod
    def updateCarrera(carrera, userId):
        conn=Connection()
        session=conn.getSession()
        _carrera=session.query(Carrera).filter(Carrera.id == carrera.id).first()
        if _carrera:
            if (_carrera.descripcion != carrera.descripcion):
                _carrera.descripcion = carrera.descripcion
                modificado=True
            if (_carrera.duracion != carrera.duracion):
                _carrera.duracion = carrera.duracion
                modificado=True
        
        if modificado:
            try:
                _carrera.modificacion_usuario_id = userId
                _carrera.fecha_modificacion = datetime.now()
                session.commit()
                return {'message': 'Carrera modificada correctamente'}
            except SQLAlchemyError as e:
                return {'message': 'La carrera no pudo ser guardado'} 
            finally:
                session.close()
                conn.closeConnection()

    def to_dict(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'duracion': self.duracion,
            'fecha_creacion': self.fecha_creacion,
            'creacion_usuario_id': self.creacion_usuario_id,
            'fecha_modificacion': self.fecha_modificacion,
            'modificacion_usuario_id': self.modificacion_usuario_id
        }