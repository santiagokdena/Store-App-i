from flask import Flask
from flask_login import LoginManager
import os
from mongoengine import *
from flask_mongoengine import MongoEngine
db=MongoEngine()


def create_app():
    app=Flask(__name__)
    app.secret_key = 'super secret key'
    app.config['MONGODB_SETTINGS'] = {
    'db': 'DRUGSTORE',
    'host': "mongodb+srv://scadenaa:pochaluLU21*@cluster0.kpjffa5.mongodb.net/?retryWrites=true&w=majority"
}
    db.init_app(app)

    from .views import views    
    from .auth import auth
    from .orders import orders

    

    app.register_blueprint(views,url_prefix='/') 
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(orders,url_prefix='/')
    
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.objects(pk=id).first()
    
    return app
