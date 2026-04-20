from config import ENRON_DATABASE_PATH, SENT_FOLDER, LOG_DIR
from enron_pkg import load_emails, print_summary
from enron_pkg.email_parser import get_unique_addresses
from graph_pkg import graph
from graph_pkg.graph import Graph


def main():
    # Avaliação prévia do conjunto de dados
    frequency = load_emails(ENRON_DATABASE_PATH, sent_folder=SENT_FOLDER, log_dir=LOG_DIR)
    print_summary(frequency)

    # Requisito 1: Construção do grafo direcionado, ponderado e rotulado
    addresses = get_unique_addresses(frequency)
    index_of = {address: index for index, address in enumerate(addresses)}

    graph = Graph(len(addresses))

    for index, address in enumerate(addresses):
        graph.update_information(index, address)

    for (sender, recipient), weight in frequency.items():
        graph.create_adjacency(index_of[sender], index_of[recipient], weight)

    print(f"\nGrafo construído com {graph.size} vértices.")

    # Requisito 2: Análise do grafo
    print("\nAnálise do grafo:")
    print(f"\na) Número de vértices: {graph.size}")
    print(f"b) Número de arestas: {graph.edge_count()}")

    print(f"\nc) Top 20 — maior grau de saída:")
    for label, degree in graph.top_out_degree(20):
        print(f"  {label}: {degree}")

    print(f"\nd) Top 20 — maior grau de entrada:")
    for label, degree in graph.top_in_degree(20):
        print(f"  {label}: {degree}")

if __name__ == "__main__":
    main()