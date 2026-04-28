"""
Arquivo responsável por funções auxiliares para a interface interativa com o usuário.
"""


def get_menu_option(valid_options: list[str], prompt: str = "Escolha uma opção: ") -> str:
    """Solicita e valida uma opção do menu."""
    while True:
        option = input(prompt).strip()
        if option in valid_options:
            return option
        print("Opção inválida. Tente novamente.\n")


def get_valid_email(emails: dict[str, int], prompt: str) -> str | None:
    """Solicita um email válido ao usuário."""
    while True:
        email: str = input(prompt).strip().lower()
        if email == "sair":
            return None
        if email in emails:
            return email
        print(f"  Endereço '{email}' não encontrado. Tente novamente.\n")
