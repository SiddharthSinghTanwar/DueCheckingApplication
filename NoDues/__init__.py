from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import NoDues.instance.config as config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Configuration (you can load it from an external config.py file)
# Access the configuration settings from config.py
# app.config['SECRET_KEY'] = config.SECRET_KEY
# app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from NoDues import routes
