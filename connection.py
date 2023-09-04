from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from config import URL_DB, TRACK_MODIFICATIONS, USER_DB, PASS_DB, MOTOR_DB, NAME_DB

class Connection:
    def __init__(self) -> None:
        #self.url=URL.create(drivername="postgresql",
        #                    username=USER_DB,
        #                    password=PASS_DB,
        #                   host=POSTGRES_HOST,
        #                    database=POSTGRES_DATABASE
        #                  )
        self.uriDB=MOTOR_DB+'://'+USER_DB+':'+PASS_DB+'@'+URL_DB+'/'+NAME_DB
        
        print("me conecte!")
        print("agrego algo para q1ue cambie")
        self.engine=create_engine(self.uriDB)
        Session=sessionmaker(bind=self.engine)   
        self.session=Session()

    def getSession(self):
        return self.session
    
    def closeConnection(self):
            self.engine.dispose()

#class Connection:
#    def __init__(self) -> None:
#        self.uriDB=MOTOR_DB+'://'+USER_DB+':'+PASS_DB+'@'+URL_DB+'/'+NAME_DB
#        self.engine=create_engine(self.uriDB)
#        Session=sessionmaker(bind=self.engine)
#        self.session=Session()

#    def getSession(self):
#       return self.session
    
#    def closeConnection(self):
#        self.engine.dispose()
