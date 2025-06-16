from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from src.configs.config_globais import URL_BANCO_DE_DADOS

"""
Este arquivo define as configurações de conexão e inicialização do banco de dados
para o sistema de loja de hardware, utilizando SQLAlchemy como ORM. Configura
a engine SQLite, sessão de banco de dados e fornece funcionalidade para
criação automática das tabelas através da classe Base declarativa.
"""

Base = declarative_base()

if URL_BANCO_DE_DADOS:
    print(f"Conectando ao banco de dados: {URL_BANCO_DE_DADOS}")
else:
    print("Nenhuma URL de banco de dados fornecida, usando SQLite local.")

engine = create_engine(
    URL_BANCO_DE_DADOS or "sqlite:///hardware_store.db", echo=True)

if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(bind=engine)


def iniciar_bd():
    Base.metadata.create_all(engine)
