from flask import Blueprint, render_template, redirect, request, url_for, flash
from app.models import Usuarios, Produtos, Categorias
from app import db
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import re

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/', methods=["GET"])
def index():
	return render_template('index.html')

@usuario_bp.route("/cadastrarUser", methods=["GET", "POST"])
def cadastrarUser():

	if request.method == "POST":
		nomeUser = request.form["nomeUser"]
		analisarUser = Usuarios.query.filter(Usuarios.nomeUser == nomeUser).first()

		if analisarUser:
			flash("Nome de usuário já existe!", "warning")
			return redirect(url_for("usuario.index"))

		email = request.form["emailUser"]
		analisarEmail = Usuarios.query.filter(Usuarios.email == email).first()
		if analisarEmail:
			flash("Email já registrado", "warning")
			return redirect(url_for("usuario.index"))
		if  not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
			flash("E-mail inválido!", "error")
			return redirect(url_for('usuario.index'))

		senhaDigitada = request.form["senhaUser"]
		if len(senhaDigitada) < 8:
			flash("A senha deve ter pelo menos 8 caracteres.", "error")
			return redirect(url_for('usuario.index'))
		configSenha = PasswordHasher(
			time_cost=4,
			memory_cost=64*1024,
			parallelism=4
			)
		senhaHash = configSenha.hash(senhaDigitada)

		novo_usuario = Usuarios(nomeUser=nomeUser, email=email, senhaHash=senhaHash)
		db.session.add(novo_usuario)
		db.session.commit()
		flash("Usuário cadastrado com sucesso!", "success")
		return redirect(url_for("usuario.index"))

	return render_template("index.html")


@usuario_bp.route('/loginUser', methods=["GET", "POST"])
def loginUser():
	if request.method == "POST":
		email = request.form["emailLogin"]
		if  not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
			flash("E-mail inválido!", "error")
			return redirect(url_for('usuario.index'))
		usuario = Usuarios.query.filter_by(email=email).first()
		if not usuario:
			flash("Email não registrado no Sistema", "warning")
			return redirect(url_for("usuario.index"))

		senhaDigitada = request.form["senhaLogin"]
		if len(senhaDigitada) < 8:
			flash("A senha deve ter pelo menos 8 caracteres.", "error")
			return redirect(url_for('usuario.index'))
		configSenha = PasswordHasher(
			time_cost=4,
			memory_cost=64*1024,
			parallelism=4
			)

		try:
			configSenha.verify(usuario.senhaHash, senhaDigitada)
			flash("Login realizado com sucesso!", "success")
			return redirect(url_for("usuario.perfil", usuario_id=usuario.id))
		except VerifyMismatchError:
			flash("Senha incorreta!", "error")
			return redirect(url_for("usuario.index"))

	return render_template("index.html")


@usuario_bp.route("/perfil/<int:usuario_id>")
def perfil(usuario_id):
	usuario = Usuarios.query.get_or_404(usuario_id)
	return render_template("perfil.html", usuario=usuario)