import os
import pickle
from config import ENRON_DATABASE_PATH, SENT_FOLDER, LOG_DIR, CACHE_DIR, CACHE_PATH
from enron_pkg import load_emails, get_unique_addresses, print_summary
from graph_pkg import Graph
from cli import interactive_menu
from cli_utils import get_menu_option


def load_frequency() -> dict[tuple[str, str], int]:
    """Carrega frequências do cache ou faz o parsing dos emails."""
    if os.path.isfile(CACHE_PATH):
        print("Encontrado cache de dados anterior.")
        option: str = get_menu_option(["1", "2"], prompt=(
            "1. Usar cache (carregamento rápido)\n"
            "2. Reprocessar emails do dataset\n"
            "Escolha uma opção: "
        ))

        if option == "1":
            with open(CACHE_PATH, "rb") as file:
                frequency = pickle.load(file)
            print("Dados carregados do cache.")
            return frequency

    frequency: dict[tuple[str, str], int] = load_emails(
        database_path=ENRON_DATABASE_PATH,
        sent_folder=SENT_FOLDER,
        log_dir=LOG_DIR
    )
    print_summary(frequency)

    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_PATH, "wb") as file:
        pickle.dump(frequency, file)
    print(f"Cache salvo em: {CACHE_PATH}")
    return frequency


def main():
    frequency: dict[tuple[str, str], int] = load_frequency()

    # Requisito 1: Construção do grafo direcionado, ponderado e rotulado
    addresses: list[str] = get_unique_addresses(frequency)
    index_of: dict[str, int] = {address: index for index, address in enumerate(addresses)}
    graph: Graph = Graph(len(addresses))
    for index, address in enumerate(addresses):
        graph.update_information(index, address)
    for (sender, recipient), weight in frequency.items():
        graph.create_adjacency(index_of[sender], index_of[recipient], weight)
    print(f"\nGrafo construído com {graph.size} vértices.")

    # Menu interativo
    interactive_menu(graph, index_of)


if __name__ == "__main__":
    main()