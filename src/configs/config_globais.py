from dotenv import load_dotenv as carregar_arquivo_dotenv
from os import getenv

"""
Este arquivo gerencia as configurações e variáveis de ambiente do sistema
de loja de hardware, utilizando python-dotenv para carregar variáveis
do arquivo .env. Centraliza o acesso a configurações sensíveis como
URLs de banco de dados e outras configurações do ambiente.
"""

carregar_arquivo_dotenv()

URL_BANCO_DE_DADOS = getenv("URL_BANCO_DE_DADOS")
