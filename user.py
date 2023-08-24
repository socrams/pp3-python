from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.exc import SQLAlchemyError
import jwt
import hashlib
from datetime import datetime, timedelta
from connection import Connection
from config import SIGNATURE_KEY
Base=declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    enabled = Column(Boolean)
    full_name = Column(String(255))
    password = Column(String(255))
    phone = Column(String(255))
    status = Column(Boolean)
    creation_date = Column(TIMESTAMP)
    creation_user_id = Column(Integer)
    should_reset_password = Column(Boolean)
    last_reset_password = Column(TIMESTAMP)
    last_update = Column(TIMESTAMP)
    last_update_user_id=Column(Integer)

    @staticmethod
    def getUsers():
        conn=Connection()
        session=conn.getSession()
        allUser=session.query(User).filter(User.enabled == 1).all()
        session.close()
        conn.closeConnection()
        return [u.to_dict() for u in allUser]
    
    @staticmethod
    def getUserById(_id):
        conn=Connection()
        session=conn.getSession()
        _user=session.query(User).filter(User.id==_id).first()
        session.close()
        conn.closeConnection()
        return _user.to_dict()
    
    @staticmethod
    def deleteUser(id, nUserId):
        conn=Connection()
        session=conn.getSession()
        _user = session.query(User).filter(User.id==id).first()
        _user.status = False
        _user.enabled = False
        _user.last_update = datetime.now()
        _user.last_update_user_id = nUserId
        session.commit()
        return True

    @staticmethod
    def addUser(user):
        conn=Connection()
        session=conn.getSession()
        try:
            session.add(user)
            session.commit()
            return {'message':'Usuario agregado correctamente.'}
        except SQLAlchemyError as e:
            return {'message':'Error al intentar guardar el nuevo usuario.'}
        finally:
            session.close()
            conn.closeConnection()

    @staticmethod
    def updateUser(user):
        modificado=False
        conn=Connection()
        session=conn.getSession()
        _userOld=session.query(User).filter(User.id==user.id).first()
        if _userOld:
            if _userOld.name != user.name:
                _userOld.name = user.name
                modificado=True

            if _userOld.full_name != user.full_name:
                _userOld.full_name = user.full_name
                modificado=True

            if _userOld.email != user.email:
                _userOld.email = user.email
                modificado=True

            if _userOld.enabled != user.enabled:
                _userOld.enabled = user.enabled
                modificado=True

            if _userOld.password != user.password:
                _userOld.password = user.password
                modificado=True

            if _userOld.phone != user.phone:
                _userOld.phone = user.phone
                modificado=True

            if _userOld.status != user.status:
                _userOld.status = user.status
                modificado=True
            
            if  modificado:
                try:
                    session.commit()
                    return {'message':'Registro: '+str(_userOld.id)+' modificado correctamente.'}
                except SQLAlchemyError as e:
                    return {'message':'Error la intentar updatear el registro: ' +str(_userOld.id)}
                finally:
                    session.close()
                    conn.closeConnection()

    @staticmethod
    def login(mail, password):
        conn=Connection()
        session=conn.getSession()
        print(mail)
        print(password)
        _user=session.query(User).filter(User.email==mail).first()    
        session.close()
        conn.closeConnection()
        print(_user.password)
        if password == _user.password:
            print('son iguales')
            return _user
        else:
            return None

    @staticmethod
    def setLastLogin(id):
        conn=Connection()
        try:
            session=conn.getSession()
            _user = session.query(User).filter(User.id==id).first()
            if _user:
                _user.last_update=datetime.now()
                session.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            print(f"Error al intentar actualizar el usuario. Detalle: {str(e)}")
        finally:
            session.close()
            conn.closeConnection()

    def generar_token(usuario_id):
        tiempo_expiracion = datetime.utcnow() + timedelta(minutes=30) 
        payload = {
            'usuario_id': usuario_id,
            'exp': tiempo_expiracion
        }
        token = jwt.encode(payload, SIGNATURE_KEY, algorithm='HS256') 
        return token

    def validateToken(token):
        try:
            payload = jwt.decode(token, SIGNATURE_KEY, algorithms=['HS256'])
            user_id = payload['usuario_id']

        except jwt.ExpiredSignatureError:
            return {'message':'Usuario expirado.'}
        except jwt.InvalidTokenError:
            return {'message':'Token invalido.'}
        
        return True

    def getUserIDFromToken(token):
        try:
            payload = jwt.decode(token, SIGNATURE_KEY, algorithms=['HS256'])
            user_id = payload['usuario_id']
        except jwt.ExpiredSignatureError:
            return -1
        except jwt.InvalidTokenError:
            return -99
        return user_id

    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'enabled': self.enabled,
            'full_name': self.full_name,
            'password': self.password,
            'phone': self.phone,
            'status': self.status,
            'creation_date': self.creation_date,
            'creation_user_id': self.creation_user_id,
            'should_reset_password': self.should_reset_password,
            'last_reset_password': self.last_reset_password,
            'last_update': self.last_update
        }
