from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, DATE, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from connection import Connection
from config import SIGNATURE_KEY
Base=declarative_base()

class MateriaProfesor(Base):
    __tablename__= 'MATERIAS_PROFESOR'

    id = Column(Integer, primary_key=True)
    materia_id = Column(Integer)
    comision = Column(Integer)
    curso = Column(String(1))
    profesor = Column(String(500))
    desde = Column(DATE)
    hasta = Column(DATE)



    def to_dict(self):
        return {
            'id': self.id,
            'materia_id': self.materia_id,
            'comsion': self.comision,
            'curso': self.curso,
            'profesor': self.profesor,
            'desde': self.desde,
            'hasta': self.hasta
        }