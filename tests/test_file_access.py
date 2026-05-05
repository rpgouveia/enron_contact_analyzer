"""
Script de diagnóstico para verificar se os arquivos de e-mail
são reconhecidos corretamente pelo sistema operacional.

Contexto: ao extrair o dataset Enron (tar.gz) no Windows, os arquivos
podem receber um ponto no final do nome (ex: '1.' ao invés de '1').
Isso faz com que os.path.isfile() retorne False e open() falhe,
impedindo a leitura dos e-mails.
"""

import os
from dotenv import load_dotenv

load_dotenv()
path = os.getenv("ENRON_DATABASE_PATH")
sent = os.getenv("SENT_FOLDER")

test = os.path.join(path, "allen-p", sent)
files = os.listdir(test)

print(f"Total de arquivos: {len(files)}")
print(f"Primeiros 5: {files[:5]}")

for filename in files[:5]:
    filepath = os.path.join(test, filename)
    is_file = os.path.isfile(filepath)
    starts_dot = filename.startswith(".")
    print(f"  {filename} → isfile={is_file}, startswith_dot={starts_dot}")