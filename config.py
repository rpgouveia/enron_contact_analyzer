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

required_variables: dict[str, str | None] = {
    "ENRON_DATABASE_PATH": ENRON_DATABASE_PATH,
    "SENT_FOLDER": SENT_FOLDER,
    "LOG_DIR": LOG_DIR,
}

for variable_name, variable_value in required_variables.items():
    if variable_value is None:
        raise ValueError(
            f"Variável de ambiente obrigatória '{variable_name}' não definida. "
            f"Configure no arquivo .env"
        )
