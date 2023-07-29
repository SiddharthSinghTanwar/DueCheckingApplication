from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ea77a2c1cff84971c247e008b1a749fd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from nodues import routes

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# # import NoDues.instance.config as config
# from flask_bcrypt import Bcrypt
# # from flask_login import LoginManager

# db = SQLAlchemy()
# bcrypt = Bcrypt()
# # login_manager = LoginManager()

# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'ea77a2c1cff84971c247e008b1a749fd'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#     db.init_app(app)
#     bcrypt.init_app(app)
#     # login_manager.init_app(app)


#     return app
