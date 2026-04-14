"""
Módulo responsável por ler e processar os e-mails da base Enron.
Cada arquivo dentro de sent é um e-mail em texto puro (RFC 822).
"""

import os
import email
from email import policy
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict
from tqdm import tqdm


@dataclass
class Email:
    """Representa um e-mail parseado com remetente e destinatários."""

    sender: str
    recipients: list[str]

    @staticmethod
    def from_file(filepath: str) -> "Email | None":
        """
        Lê um arquivo de e-mail e retorna um objeto Email.
        Retorna None se não conseguir extrair remetente ou destinatários.
        """
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                msg = email.message_from_file(file, policy=policy.default)
        except Exception as error:
            print(f"[AVISO] Erro ao ler {filepath}: {error}")
            return None

        sender = Email.__extract_address(msg.get("From", ""))
        if sender is None:
            return None

        recipients = []
        for header in ("To", "Cc", "Bcc"):
            raw = msg.get(header, "")
            if raw:
                recipients.extend(Email.__extract_addresses(raw))

        if not recipients:
            return None

        return Email(sender=sender, recipients=recipients)

    @staticmethod
    def __extract_address(raw: str) -> str | None:
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
            address = raw[start:end].strip().lower()
        else:
            address = raw.strip().lower()

        return address if "@" in address else None

    @staticmethod
    def __extract_addresses(raw: str) -> list[str]:
        """
        Extrai múltiplos endereços de uma string separada por vírgulas.
        Ex: 'a@enron.com, B <b@enron.com>' → ['a@enron.com', 'b@enron.com']
        """
        addresses = []
        raw = raw.replace("\n", " ").replace("\r", " ")
        for part in raw.split(","):
            address = Email.__extract_address(part)
            if address:
                addresses.append(address)
        return addresses


def load_emails(
            database_path: str, 
            sent_folder: str = "sent", 
            log_dir: str = "logs"
        ) -> dict[tuple[str, str], int]:
    """
    Percorre todas as pastas de usuários no dataset e lê os e-mails
    da pasta 'sent' de cada um.

    Args:
        database_path: caminho raiz do dataset (ex: './enron_mail_database')
        sent_folder: nome da subpasta de enviados (padrão: 'sent')
        log_dir: diretório onde salvar o log de arquivos ignorados

    Retorna:
        Um dicionário onde:
            chave = (remetente, destinatário)
            valor = número de e-mails enviados de remetente para destinatário
    """
    frequency = defaultdict(int)
    total_emails = 0
    skipped_files = []

    if not os.path.isdir(database_path):
        print(f"[ERRO] Diretório não encontrado: {database_path}")
        return dict(frequency)

    user_dirs = sorted(
        entry for entry in os.listdir(database_path)
        if os.path.isdir(os.path.join(database_path, entry)) and not entry.startswith(".")
    )

    print(f"Encontrados {len(user_dirs)} usuários no dataset.\n")

    for user_dir in tqdm(user_dirs, desc="Usuários", unit="usr"):
        sent_path = os.path.join(database_path, user_dir, sent_folder)

        if not os.path.isdir(sent_path):
            continue

        email_files = sorted(
            filename for filename in os.listdir(sent_path)
            if os.path.isfile(os.path.join(sent_path, filename))
            and not filename.startswith(".")
        )

        for email_file in tqdm(
            email_files,
            desc=f"  {user_dir}",
            unit="email",
            leave=False,
        ):
            filepath = os.path.join(sent_path, email_file)
            parsed = Email.from_file(filepath)

            if parsed is None:
                skipped_files.append(filepath)
                continue

            total_emails += 1
            for recipient in parsed.recipients:
                frequency[(parsed.sender, recipient)] += 1

    print(f"\nTotal de e-mails processados: {total_emails}")
    print(f"Total de e-mails ignorados: {len(skipped_files)}")
    print(f"Total de conexões únicas (remetente → destinatário): {len(frequency)}")

    if skipped_files:
        _save_skipped_log(skipped_files, log_dir)

    return dict(frequency)


def _save_skipped_log(skipped_files: list[str], log_dir: str):
    """Salva a lista de arquivos ignorados em um arquivo de log com timestamp."""
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(log_dir, f"skipped_emails_{timestamp}.log")

    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"Arquivos ignorados durante o parsing — {timestamp}\n")
        log_file.write(f"Total: {len(skipped_files)}\n")
        log_file.write("=" * 50 + "\n\n")
        for filepath in skipped_files:
            log_file.write(f"{filepath}\n")

    print(f"Log de arquivos ignorados salvo em: {log_path}")


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

    top_pairs = sorted(frequency.items(), key=lambda item: item[1], reverse=True)[:10]
    print(f"\nTop 10 pares com mais mensagens:")
    for (sender, recipient), count in top_pairs:
        print(f"  {sender} → {recipient}: {count} mensagem(ns)")