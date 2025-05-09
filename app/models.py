from sqlalchemy.orm import backref
from app import db

# Tabelas de Usuarios
# Tabelas de Produtos
class Usuarios(db.Model):
	__tablename__ = "usuarios"
	id = db.Column(db.Integer, primary_key=True)
	nomeUser = db.Column(db.String(50), nullable=False)
	email = db.Column(db.Text, nullable=False)
	senhaHash = db.Column(db.Text, nullable=False)

class Categorias(db.Model):
	__tablename__ = "categorias"
	id = db.Column(db.Integer, primary_key=True)
	nomeCategoria = db.Column(db.String(50))

class Produtos(db.Model):
	__tablename__ = "produtos"
	id = db.Column(db.Integer, primary_key=True)
	nomeProduto = db.Column(db.String(50), nullable=False)
	descricao = db.Column(db.Text)
	preco = db.Column(db.Numeric(10,2))
#                                                                  APÓS SER DELETADO, COLOCORA UM NULL
	categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id', ondelete='SET NULL'))
	categoria = db.relationship("Categorias", backref=backref('produtos'))

	usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'))
	usuario = db.relationship("Usuarios", backref=backref('produtos'))

