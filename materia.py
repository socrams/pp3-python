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
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'carrera_id': self.carrera_id,
            'anio': self.anio,
            'descripcion': self.descripcion,
            'vigencia': self.vigencia
        }