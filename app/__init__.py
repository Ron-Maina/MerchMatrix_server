import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from app import models
from .extensions import api, db
from .endpoints import ns

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merchmatrix.db'
    app.config["JWT_SECRET_KEY"] = os.environ.get('FLASK_JWT_SECRET_KEY') 
    app.config["JWT_ALGORITHM"] = "HS256"

    api.init_app(app)
    db.init_app(app)
    # jwt.init_app(app)

    migrate = Migrate(app,db)



    api.add_namespace(ns)

    return app 