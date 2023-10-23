from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, insert
from connection import Connection
Base=declarative_base()

class Response(Base):
    __tablename__= 'bot_response'

    id=Column(Integer, primary_key=True)
    answer=Column(String(500))
    response=Column(String(2000))
    options=Column(String(2000))
    morequestion=Column(Boolean)
    moreoptions=Column(Boolean)

    @staticmethod   
    def getResponses():
        conn=Connection()
        session=conn.getSession()
        allresponse=session.query(Response).all()
        session.close()
        conn.closeConnection()
        return [r.to_dict() for r in allresponse]
    
    def getResponseLocal():
        conn=Connection()
        session=conn.getSession()
        allresponse=session.query(Response).all()
        session.close()
        conn.closeConnection()
        return allresponse
    
    @staticmethod
    def getResponse(_id):
        conn=Connection()
        session=conn.getSession()
        _response=session.query(Response).filter(Response.id == _id).first()
        session.close()
        conn.closeConnection()
        return _response.to_dict()
    
    @staticmethod
    def delResponse(_id):
        conn=Connection()
        session=conn.getSession()
        _response=session.query(Response).filter(Response.id == _id).first()
        if _response:
            session.delete(_response)
            session.commit()
            session.close()
            conn.closeConnection()
            return {'message':'Se elimino la respuesta.'}
        else:
            session.close()
            conn.closeConnection()
            return {'message':'No se encontró la respuesta.'}

    @staticmethod
    def addResponse(_response):
        conn=Connection()
        session=conn.getSession()
        smt = (
            insert (table='bot_response').values(answer = _response.answer, 
                             response = _response.response,
                             options = _response.options,
                             moreOptions = _response.moreOptions,
                             moreQuestion = _response.moreQuestion)
        )        
        session.execute(smt)
        session.close()
        conn.closeConnection()
        return {'message': 'insertado correctamente'}

    @staticmethod
    def updateResponse(_response):
        conn=Connection()
        session=conn.getSession()
        dbResponse = session.query(Response).filter(Response.id == _response.id).first()
        modificated = False
        print(dbResponse)
        if (dbResponse):
            if (dbResponse.answer != _response.answer):
                dbResponse.answer = _response.answer
                modificated = True

            if (dbResponse.response != _response.response):
                dbResponse.response = _response.response
                modificated = True
            
            if (dbResponse.options != _response.options):
                dbResponse.options = _response.options
                modificated = True

            if (dbResponse.morequestion != _response.morequestion):
                dbResponse.morequestion = _response.morequestion
                modificated = True
            
            if (dbResponse.moreoptions != _response.moreoptions):
                dbResponse.moreoptions = _response.moreoptions
                modificated = True

            if (modificated):
                session.commit()
                message = {'message':'Se actualizo la respuesta.'}
            else:
                message = {'message':'No se actualizo la respuesta.'}
        else:
            message = {'message': 'No se encontro la respuesta'}

        session.close()
        conn.closeConnection()
        return message    



    def to_dict(self):
        return {
            'id': self.id,
            'answer': self.answer,
            'response': self.response,
            'options': self.options,
            'morequestion': self.morequestion,
            'moreoptions': self.moreoptions
        }
