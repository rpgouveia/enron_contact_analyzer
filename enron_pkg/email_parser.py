"""
Módulo responsável por ler e processar os e-mails da base Enron.
Cada arquivo dentro de sent é um e-mail em texto puro (RFC 822).
"""

import os
import email
from email import policy
from collections import defaultdict
from tqdm import tqdm


def parse_email_file(filepath: str) -> tuple[str | None, list[str]]:
    """
    Lê um arquivo de e-mail e extrai o remetente e os destinatários.

    Retorna:
        (sender, recipients) — sender é uma string (endereço),
        recipients é uma lista de endereços (To + Cc + Bcc).
        Retorna (None, []) se não conseguir extrair.
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            msg = email.message_from_file(f, policy=policy.default)
    except Exception as e:
        print(f"[AVISO] Erro ao ler {filepath}: {e}")
        return None, []

    sender = _extract_address(msg.get("From", ""))

    recipients = []
    for header in ("To", "Cc", "Bcc"):
        raw = msg.get(header, "")
        if raw:
            recipients.extend(_extract_addresses(raw))

    return sender, recipients


def _extract_address(raw: str) -> str | None:
    """
    Extrai um único endereço de e-mail de uma string.
    Ex: 'John Doe <john.doe@enron.com>' → 'john.doe@enron.com'
    """
    raw = raw.strip()
    if not raw:
        return None

    if "<" in raw and ">" in raw:
        start = raw.index("<") + 1
        end = raw.index(">")
        addr = raw[start:end].strip().lower()
    else:
        addr = raw.strip().lower()

    return addr if "@" in addr else None


def _extract_addresses(raw: str) -> list[str]:
    """
    Extrai múltiplos endereços de uma string separada por vírgulas.
    Ex: 'a@enron.com, B <b@enron.com>' → ['a@enron.com', 'b@enron.com']
    """
    addresses = []
    raw = raw.replace("\n", " ").replace("\r", " ")
    for part in raw.split(","):
        addr = _extract_address(part)
        if addr:
            addresses.append(addr)
    return addresses


def load_emails(database_path: str, sent_folder: str = "sent") -> dict[tuple[str, str], int]:
    """
    Percorre todas as pastas de usuários no dataset e lê os e-mails
    da pasta 'sent' de cada um.

    Args:
        database_path: caminho raiz do dataset (ex: './enron_mail_database')
        sent_folder: nome da subpasta de enviados (padrão: 'sent')

    Retorna:
        Um dicionário onde:
            chave = (remetente, destinatário)
            valor = número de e-mails enviados de remetente para destinatário
    """
    frequency = defaultdict(int)
    total_emails = 0
    total_errors = 0

    if not os.path.isdir(database_path):
        print(f"[ERRO] Diretório não encontrado: {database_path}")
        return dict(frequency)

    user_dirs = sorted(
        d for d in os.listdir(database_path)
        if os.path.isdir(os.path.join(database_path, d)) and not d.startswith(".")
    )

    print(f"Encontrados {len(user_dirs)} usuários no dataset.\n")

    for user_dir in tqdm(user_dirs, desc="Usuários", unit="usr"):
        sent_path = os.path.join(database_path, user_dir, sent_folder)

        if not os.path.isdir(sent_path):
            continue

        email_files = sorted(
            f for f in os.listdir(sent_path)
            if os.path.isfile(os.path.join(sent_path, f)) and not f.startswith(".")
        )

        for email_file in tqdm(
            email_files,
            desc=f"  {user_dir}",
            unit="email",
            leave=False,
        ):
            filepath = os.path.join(sent_path, email_file)
            sender, recipients = parse_email_file(filepath)

            if sender is None or not recipients:
                total_errors += 1
                continue

            total_emails += 1
            for recipient in recipients:
                # Evitar contar e-mails enviados para si mesmo (auto-envio)
                if recipient != sender:
                    frequency[(sender, recipient)] += 1

    print(f"\nTotal de e-mails processados: {total_emails}")
    print(f"Total de e-mails ignorados (sem remetente/destinatário): {total_errors}")
    print(f"Total de conexões únicas (remetente → destinatário): {len(frequency)}")

    return dict(frequency)


def get_unique_addresses(frequency: dict[tuple[str, str], int]) -> list[str]:
    """
    Extrai a lista ordenada de todos os endereços de e-mail únicos
    presentes no dicionário de frequências.
    """
    addresses = set()
    for sender, recipient in frequency:
        addresses.add(sender)
        addresses.add(recipient)
    return sorted(addresses)


def print_summary(frequency: dict[tuple[str, str], int]):
    """Imprime um resumo dos dados extraídos."""
    addresses = get_unique_addresses(frequency)
    total_msgs = sum(frequency.values())

    print(f"\n{'='*50}")
    print(f"RESUMO DO DATASET")
    print(f"{'='*50}")
    print(f"Endereços únicos (futuros vértices): {len(addresses)}")
    print(f"Conexões únicas (futuras arestas):   {len(frequency)}")
    print(f"Total de mensagens enviadas:          {total_msgs}")
    print(f"{'='*50}")

    top_pairs = sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:10]
    print(f"\nTop 10 pares com mais mensagens:")
    for (sender, recipient), count in top_pairs:
        print(f"  {sender} → {recipient}: {count} mensagem(ns)")
