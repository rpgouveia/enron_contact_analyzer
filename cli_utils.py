"""
Arquivo responsável por funções auxiliares para a interface interativa com o usuário.
"""
import os
from datetime import datetime


def get_menu_option(valid_options: list[str], prompt: str = "Escolha uma opção: ") -> str:
    """Solicita e valida uma opção do menu."""
    while True:
        option = input(prompt).strip()
        if option in valid_options:
            return option
        print("Opção inválida. Tente novamente.\n")


def get_valid_email(emails: dict[str, int], prompt: str) -> str | None:
    """Solicita um email válido ao usuário. Retorna None se digitar 'sair'."""
    while True:
        email: str = input(prompt).strip().lower()
        if email == "sair":
            return None
        if email in emails:
            return email
        print(f"  Endereço '{email}' não encontrado. Tente novamente.\n")


def ask_yes_no(prompt: str) -> bool:
    """Solicita uma confirmação sim/não ao usuário."""
    response = input(prompt).strip().lower()
    return response.startswith("s")


def save_result_log(content: str, prefix: str, log_dir: str = "logs"):
    """Salva o resultado de uma operação em um arquivo de log com timestamp."""
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(log_dir, f"{prefix}_{timestamp}.log")

    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write(content)

    print(f"Resultado salvo em: {log_path}")