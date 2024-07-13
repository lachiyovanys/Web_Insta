from flask import Flask
from modules.flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config["SESSION_TYPE"] = "filesystem"

    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    

    return app