from config import ENRON_DATABASE_PATH, SENT_FOLDER, LOG_DIR
from enron_pkg import load_emails, get_unique_addresses, print_summary
from graph_pkg import Graph, graph


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

    # Requisito 2: Informações gerais do grafo
    print("\nAnálise do grafo:")
    print(f"\nNúmero de vértices: {graph.size}")
    print(f"Número de arestas: {graph.edge_count()}")
    graph.print_top_out_degree(20)
    graph.print_top_in_degree(20)
    
    # Requisito 3: Busca em profundidade (DFS) — alcançabilidade entre dois indivíduos
    # TODO: Implementar a função de DFS e chamar aqui para testar


    # Requisito 4: Busca em largura (BFS) — alcançabilidade entre dois indivíduos    
    # Origem e Destino para o teste de sucesso
        # origin = "drew.fossum@enron.com"
        # destination = "mary.miller@enron.com"
    print(f"\nBusca em largura (BFS) — alcançabilidade entre dois indivíduos")
    print("Digite 'sair' para encerrar.\n")

    while True:
        origin = input("Remetente (email): ").strip().lower()
        if origin == "sair":
            break

        destination = input("Destinatário (email): ").strip().lower()
        if destination == "sair":
            break

        if origin not in index_of:
            print(f"  Endereço '{origin}' não encontrado no grafo.\n")
            continue

        if destination not in index_of:
            print(f"  Endereço '{destination}' não encontrado no grafo.\n")
            continue

        graph.print_bfs_reach(index_of[origin], index_of[destination])
        print()


if __name__ == "__main__":
    main()