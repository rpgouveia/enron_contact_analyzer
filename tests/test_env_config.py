"""
Script de diagnóstico para verificar se as variáveis de ambiente
estão configuradas corretamente e se os caminhos do dataset são acessíveis.

Contexto: criado para diagnosticar problemas de compatibilidade
entre Linux e Windows na leitura do dataset Enron.
"""

import os
from dotenv import load_dotenv

load_dotenv()
path = os.getenv("ENRON_DATABASE_PATH")
sent = os.getenv("SENT_FOLDER")

print(f"Path: [{path}]")
print(f"Sent: [{sent}]")

test = os.path.join(path, "allen-p", sent)
print(f"Full: [{test}]")
print(f"Exists: {os.path.isdir(test)}")
print(f"Contents: {os.listdir(test) if os.path.isdir(test) else 'N/A'}")