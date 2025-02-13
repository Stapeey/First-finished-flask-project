#a website foldert python packaggé csinálja, lehet így importálni
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
DB_NAME = "database.db"


def updater():
    from .views import finalload
    if finalload != []:
        return finalload[:]
    else:
        return False


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'randomblabla' #ez fontos cookieknál
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
    db.init_app(app)


    app.jinja_env.globals.update(updater=updater)


    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')#ez fogyatékosan műkszik

    from .models import User, Note

    with app.app_context():
        db.create_all()
    

    return app
