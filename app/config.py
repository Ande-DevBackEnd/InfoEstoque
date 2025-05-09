import pymysql
from sqlalchemy import create_engine, text


host = 'localhost'
user = 'root'
password = "!Ande4350n"
database = "sistema_produtos"

class Database:
	def createDatasabe():
		SQLALCHEMY_DATABASE_URI = create_engine(f'mysql+pymysql://{user}:{password}@{host}')
		with SQLALCHEMY_DATABASE_URI.connect() as conn:       
			conn.execute(text(f'Create Database If Not Exists {database}'))

	createDatasabe()
	SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@{host}/{database}'
	SQLALCHEMY_TRACK_MODIFICATIONS = False