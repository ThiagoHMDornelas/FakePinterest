# criar as rotas para o site (os links)
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import os

from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Foto



@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), form_login.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for("perfil", id_usuario=usuario.id))

    return render_template("homepage.html", form=form_login)


@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criar_conta = FormCriarConta()
    if form_criar_conta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode("utf-8")
        usuario = Usuario(username = form_criar_conta.username.data,
                          email = form_criar_conta.email.data,
                          senha = senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=form_criar_conta)


@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # o usuario ta vendo o perfil dele
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # salvar o arquivo dentro da pasta certa
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   app.config["UPLOAD_FOLDER"],
                                   nome_seguro)
            arquivo.save(caminho)
            # criar a foto no banco com o item "imagem" sendo o nome do arquivo
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            return redirect(url_for("perfil", id_usuario=id_usuario))

        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
       usuario = Usuario.query.get(int(id_usuario))
       return render_template("perfil.html", usuario=usuario, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
     fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
     return render_template("feed.html", fotos=fotos)