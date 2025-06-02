from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env local

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e09cd9eddebc52208c670ea53536bf90'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///comunidade.db")
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

# Instâncias
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage' # passar o nome do route q gerencia o login. neste caso, o login q feito no "def homepage()"
# login.login_message = 'faça o login para continuar'
# login.login_message_category = 'alert-info'

from fakepinterest import routes