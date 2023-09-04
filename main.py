import sys
sys.path.append('c:\python310\lib\site-packages')

from flask import Flask
from flask_cors import CORS

from config import LANGUAJE, SIGNATURE_KEY

from auth.routes import auth_bp
from careers.routes import careers_bp
from chats.routes import chats_bp
from responses.routes import response_bp
from users.routes import user_bp

# import enchant

app = Flask(__name__)

CORS(app)
#incluimos los routes de cada metodos
app.register_blueprint(careers_bp, url_prefix='/carrera')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(chats_bp, url_prefix='/chat')
app.register_blueprint(response_bp, url_prefix='/response')
app.register_blueprint(user_bp, url_prefix='/users')


#interpreter=enchant.Dict(LANGUAJE)
@app.route('/')
def hello():
    return "¡Hola, esta es una API Flask!"


if __name__=="__main__":
    app.run(debug=True)
    # app.run(debug=False)
