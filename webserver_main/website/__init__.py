from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, environ

db = SQLAlchemy()
#DB_NAME = "weather.db" #Could be used for local runs without docker

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sessionCookie'
#    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
    db.init_app(app)

    from .views import views 
    app.register_blueprint(views, url_prefix='/')
   
    with app.app_context():
        db.create_all()

    from .mqtt import mqttInitializer
    mqttInitializer(app)


    
    return app