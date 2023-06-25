from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, DATE, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from connection import Connection
from config import SIGNATURE_KEY
Base=declarative_base()

class Materia(Base):
    __tablename__= 'MATERIAS'

    id = Column(Integer, primary_key=True)
    carrera_id = Column(Integer)
    anio = Column(Integer)
    descripcion = Column(String(200))
    vigencia = Column(DATE)
    
    @staticmethod
    def getMateria():
        conn=Connection()
        session=conn.getSession()
        materias=session.query(Materia).all()
        session.close()
        conn.closeConnection()
        return [m.to_dict() for m in materias]
    
    @staticmethod
    def getMateriaById(id):
        conn=Connection()
        session=conn.getSession()
        materia=session.query(Materia).filter(Materia.id == id).first()
        session.close()
        conn.closeConnection()
        return materia.to_dict()        

    @staticmethod
    def addMateria(materia):
        conn=Connection()
        session=conn.getSession()
        try:
            session.add(materia)
            session.commit()
            return {'message': 'Materia agregada correctamente.'}
        except SQLAlchemyError as e:
            return {'message': 'Materia no agregada.'}
        finally:
            session.close()
            conn.closeConnection()

    @staticmethod
    def deleteMateria(id):
        conn=Connection()
        session=conn.getSession()
        materia = session.query(Materia).filter(Materia.id == id).first()
        if materia:
            session.delete(materia)
            session.commit()
            session.close()
            conn.closeConnection()
            return {'message':'Materia eliminada correctamente.'}
        else:
            session.close()
            conn.closeConnection()
            return {'message':'Materia no encontrada.'}
        
    @staticmethod
    def updateMateria(materia):
        conn=Connection()
        session=conn.getSession()
        oldMateria = session.query(Materia).filter(Materia.id == id).first()
        
        if oldMateria:
            if oldMateria.descripcion != materia.descripcion:
                oldMateria.descripcion = materia.descripcion
            
            if oldMateria.vigencia != materia.vigencia:
                oldMateria.vigencia = materia.vigencia
            
            if oldMateria.anio != materia.anio:
                oldMateria.anio = materia.anio
            
            session.commit()
            session.close()
            conn.closeConnection()
            return {'message': 'Materia modificada correctamente.'}
        else:
            session.close()
            conn.closeConnection()
            return {'message': 'Materia no encontrada para su modificacion.'}

    def to_dict(self):
        return {
            'id': self.id,
            'carrera_id': self.carrera_id,
            'anio': self.anio,
            'descripcion': self.descripcion,
            'vigencia': self.vigencia if self.vigencia is not None else None
        }