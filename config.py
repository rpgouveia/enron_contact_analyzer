"""
Arquivo de configuração do projeto.
Carrega variáveis de ambiente do arquivo .env na raiz do projeto.
"""

import os
from dotenv import load_dotenv

load_dotenv()

ENRON_DATABASE_PATH = os.getenv("ENRON_DATABASE_PATH", "./enron_mail_database")
SENT_FOLDER = os.getenv("SENT_FOLDER", "sent")
LOG_DIR = os.getenv("LOG_DIR", "logs")
