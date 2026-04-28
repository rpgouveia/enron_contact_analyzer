from config import ENRON_DATABASE_PATH, SENT_FOLDER, LOG_DIR
from enron_pkg import load_emails, get_unique_addresses, print_summary
from graph_pkg import Graph
from cli import interactive_menu


def main():
    # Avaliação prévia do conjunto de dados
    # TODO: Talvez considerar criar um binário com os dados para serem carregados mais rapidamente
    #       assim evitando a necessidade de processar os arquivos toda vez 
    frequency: dict[tuple[str, str], int] = load_emails(
        ENRON_DATABASE_PATH, 
        sent_folder=SENT_FOLDER, 
        log_dir=LOG_DIR
    )
    print_summary(frequency)

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