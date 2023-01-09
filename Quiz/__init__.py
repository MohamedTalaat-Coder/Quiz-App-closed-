import os
from flask import Flask
import mysql.connector
from mysql.connector import Error
from flask_security import Security, SQLAlchemySessionUserDatastore


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = '01101997Programmer10?'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PORT'] = 3306


    app.config.from_mapping(SECRET_KEY = "dev", DATABASE = os.path.join(app.instance_path, 'flaskr'))
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except:
        pass
    
    from . import db
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    @app.route("/")
    def hello():
        return 'hello, world'
    return app