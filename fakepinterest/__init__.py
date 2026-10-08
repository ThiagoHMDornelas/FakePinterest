from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env local

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-fakepinterest-secret-key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///comunidade.db")
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"
app.config["EXTENSOES_PERMITIDAS"] = {"png", "jpg", "jpeg", "gif"}
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024  # 4 MB
app.config["ITENS_POR_PAGINA"] = 12

# Instâncias
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage'  # passar o nome do route q gerencia o login. neste caso, o login q feito no "def homepage()"
# login.login_message = 'faça o login para continuar'
# login.login_message_category = 'alert-info'


@app.errorhandler(413)
def arquivo_muito_grande(_erro):
    return render_template("413.html"), 413


from fakepinterest import routes  # noqa: E402,F401 (import necessário para registrar rotas)
