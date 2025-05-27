# criar as rotas para o site (os links)
from flask import render_template, url_for
from fakepinterest import app
from flask_login import login_required
from fakepinterest.forms import FormLogin, FormCriarConta

@app.route("/",methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    return render_template("homepage.html", form=form_login)


@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criar_conta = FormCriarConta()
    return render_template("criarconta.html", form=form_criar_conta)

@app.route("/perfil/<usuario>")
@login_required
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)