from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import URL_DB, TRACK_MODIFICATIONS, USER_DB, PASS_DB, MOTOR_DB, NAME_DB

class Connection:
    def __init__(self) -> None:
        self.uriDB=MOTOR_DB+'://'+USER_DB+':'+PASS_DB+'@'+URL_DB+'/'+NAME_DB
        self.engine=create_engine(self.uriDB)
        Session=sessionmaker(bind=self.engine)
        self.session=Session()

    def getSession(self):
        return self.session
    

    def closeConnection(self):
        self.engine.dispose()


