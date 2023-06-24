from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, DATE, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from connection import Connection
from config import SIGNATURE_KEY
Base=declarative_base()

class CarreraInformacion(Base):
    __tablename__= 'CARRERA_INFORMACION'

    id = Column(Integer, primary_key=True)
    materia_id = Column(Integer)
    tipo = Column(Integer)
    url = Column(String(1))
    vigencia = Column(DATE)
    


    def to_dict(self):
        return {
            'id': self.id,
            'materia_id': self.materia_id,
            'tipo': self.tipo,
            'url': self.url,
            'vigencia': self.vigencia
        }