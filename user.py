from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from connection import Connection

Base=declarative_base()


class User(Base):
    __tablename__ = 'USERS'

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

    @staticmethod
    def getUsers():
        conn=Connection()
        session=conn.getSession()
        allUser=session.query(User).all()
        session.close()
        conn.closeConnection()
        return [u.to_dict() for u in allUser]
    
    @staticmethod
    def getUserById(id):
        conn=Connection()
        session=conn.getSession()
        _user=session.query(User).from_statement('SELECT * FROM USERS WHERE ID='+id)
        session.close()
        conn.closeConnection()
        return _user.to_dict()
    

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