"""
Arquivo de configuração do projeto.
Carrega variáveis de ambiente do arquivo .env na raiz do projeto.
"""

import os
from dotenv import load_dotenv

load_dotenv()

ENRON_DATABASE_PATH = os.getenv("ENRON_DATABASE_PATH")
SENT_FOLDER = os.getenv("SENT_FOLDER")
LOG_DIR = os.getenv("LOG_DIR")

required_vars = {
    "ENRON_DATABASE_PATH": ENRON_DATABASE_PATH,
    "SENT_FOLDER": SENT_FOLDER,
    "LOG_DIR": LOG_DIR,
}

for var_name, var_value in required_vars.items():
    if var_value is None:
        raise ValueError(
            f"Variável de ambiente obrigatória '{var_name}' não definida. "
            f"Configure no arquivo .env"
        )
