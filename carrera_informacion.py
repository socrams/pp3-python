from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, DATE, text, or_
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from connection import Connection
from config import SIGNATURE_KEY
Base=declarative_base()

class CarreraInformacion(Base):
    __tablename__= 'CARRERAS_INFORMACION'

    id = Column(Integer, primary_key=True)
    carrera_id = Column(Integer)
    tipo = Column(Integer)
    url = Column(String(1))
    vigencia = Column(DATE)
    
    @staticmethod
    def getCarreraInformacion():
        conn=Connection()
        session=conn.getSession()
        carreras=session.query(CarreraInformacion).filter(or_(CarreraInformacion.vigencia.is_(None), CarreraInformacion.vigencia > datetime.now())).all()
        session.close()
        conn.closeConnection()
        return [c.to_dict() for c in carreras]

    @staticmethod
    def getInformacionById(id):
        conn=Connection()
        session=conn.getSession()
        carrera=session.query(CarreraInformacion).filter(CarreraInformacion.id == id).first()
        session.close()
        conn.closeConnection()
        return carrera.to_dict()
    
    @staticmethod
    def addInformacion(carreraInformacion):
        conn=Connection()
        session=conn.getSession()
        try:
            session.add(carreraInformacion)
            session.commit()
            return {'message':'Informacion de la carrera agregada correctamente'}
        except SQLAlchemyError as e:
            return {'message':'Error al intentar persistir la informacion de la carrera'}
        finally:
            session.close()
            conn.closeConnection();
    
    @staticmethod
    def delInformacion(id):
        conn=Connection()
        session=conn.getSession()
        carrera=session.query(CarreraInformacion).filter(CarreraInformacion.id == id).first()
        if carrera:
            session.delete(carrera)
            session.commit()
            session.close()
            conn.closeConnection()
            return {'message':'Se elimino la informacion de carrera.'}
        else:
            session.close()
            conn.closeConnection()
            return {'message': 'No se encontró el ID'}
        
    @staticmethod
    def updateInformacion(carrera):
        conn=Connection()
        session=conn.getSession()
        _carrera=session.query(CarreraInformacion).filter(CarreraInformacion.id == carrera.id).first()
        if _carrera:
            if (_carrera.tipo != carrera.tipo):
                _carrera.tipo = carrera.tipo

            if (_carrera.url != carrera.url):
                _carrera.url = carrera.url

            if _carrera.vigencia != carrera.vigencia:
                _carrera.vigencia = carrera.vigencia   
        
            try:
                session.commit()
                return {'message': 'La informacion de la carrera modificada correctamente.'}
            except SQLAlchemyError as e:
                return {'message': 'La informacion de la carrera no pudo ser guardada.'} 
            finally:
                session.close()
                conn.closeConnection()

    def to_dict(self):
        return {
            'id': self.id,
            'carrera_id': self.carrera_id,
            'tipo': self.tipo,
            'url': self.url,
            'vigencia': self.vigencia
        }