from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

db = SQLAlchemy()

def create_app():
	app = Flask(__name__)
	app.secret_key = secrets.token_hex(32)

	from app.config import Database
	app.config.from_object(Database)
	db.init_app(app)

	with app.app_context():
		from app import models
		db.create_all()

	from app.route import usuario_bp
	app.register_blueprint(usuario_bp)
	
	return app
