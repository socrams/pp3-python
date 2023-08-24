from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, DATE, text, or_
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from connection import Connection
from config import SIGNATURE_KEY
Base=declarative_base()

class MateriaProfesor(Base):
    __tablename__= 'materias_profesor'

    id = Column(Integer, primary_key=True)
    materia_id = Column(Integer)
    comision = Column(Integer)
    turno = Column(String(1))
    profesor = Column(String(500))
    desde = Column(DATE)
    hasta = Column(DATE)

    @staticmethod
    def getMateriaProfesor(id):
        conn=Connection()
        session=conn.getSession()
        profesor=session.query(MateriaProfesor).filter(MateriaProfesor.materia_id == id, or_(MateriaProfesor.hasta.is_(None), MateriaProfesor.hasta > datetime.now())).all()
        session.close()
        conn.closeConnection()
        return [m.to_dict() for m in profesor]
    
    @staticmethod
    def getMateriaProfesorById(id):
        conn=Connection()
        session=conn.getSession()
        profesor=session.query(MateriaProfesor).filter(MateriaProfesor.id == id).first()
        session.close()
        conn.closeConnection()
        return profesor.to_dict()        

    @staticmethod
    def addProfesor(materiaProfesor):
        conn=Connection()
        session=conn.getSession()
        try:
            session.add(materiaProfesor)
            session.commit()
            return {'message': 'Profesor/a agregado/a correctamente.'}
        except SQLAlchemyError as e:
            return {'message': 'Profesor/a no agregado/a.'}
        finally:
            session.close()
            conn.closeConnection()

    @staticmethod
    def deleteProfesor(id):
        conn=Connection()
        session=conn.getSession()
        profesor= session.query(MateriaProfesor).filter(MateriaProfesor.id == id).first()
        if MateriaProfesor:
            session.delete(profesor)
            session.commit()
            session.close()
            conn.closeConnection()
            return {'message':'Profesor/a eliminado/a correctamente.'}
        else:
            session.close()
            conn.closeConnection()
            return {'message':'Profesor/a no encontrado/a.'}
        
    @staticmethod
    def updateProfesor(materiaProfesor):
        conn=Connection()
        session=conn.getSession()
        oldProfesor = session.query(MateriaProfesor).filter(MateriaProfesor.id == id).first()
        
        if oldProfesor:
            if oldProfesor.profesor != materiaProfesor.profesor:
                oldProfesor.profesor = materiaProfesor.profesor
            
            if oldProfesor.desde != materiaProfesor.desde:
                oldProfesor.desde = materiaProfesor.desde
            
            if oldProfesor.hasta != materiaProfesor.hasta:
                oldProfesor.hasta = materiaProfesor.hasta
            
            if oldProfesor.curso != materiaProfesor.curso:
                oldProfesor.curso = materiaProfesor.curso

            if oldProfesor.comision != materiaProfesor.comision:
                oldProfesor.comision = materiaProfesor.comision

            if oldProfesor.turno != materiaProfesor.turno:
                oldProfesor.turno = materiaProfesor.turno

            session.commit()
            session.close()
            conn.closeConnection()
            return {'message': 'Profesor/a modificado/a correctamente.'}
        else:
            session.close()
            conn.closeConnection()
            return {'message': 'Profesor/a no encontrada/a para su modificacion.'}


    def to_dict(self):
        return {
            'id': self.id,
            'materia_id': self.materia_id,
            'comsion': self.comision,
            'turno': self.turno,
            'profesor': self.profesor,
            'desde': self.desde if self.desde is not None else None,
            'hasta': self.hasta if self.hasta is not None else None
        }
