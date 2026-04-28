"""
Arquivo responsável pela interface interativa com o usuário.
"""
from graph_pkg import Graph
from cli_utils import get_valid_email, get_menu_option


def interactive_menu(graph: Graph, index_of: dict[str, int]):
    """Menu interativo principal do programa."""
    while True:
        print(f"\n{'='*50}")
        print("MENU PRINCIPAL")
        print(f"{'='*50}")
        print("1. Informações gerais do grafo")
        print("2. Busca em largura (BFS)")
        print("3. Busca em profundidade (DFS)")
        print("0. Sair")
        print(f"{'='*50}")

        option: str = get_menu_option(["0", "1", "2", "3"])

        if option == "1":
            print_graph_info(graph)
        elif option == "2":
            interactive_bfs(graph, index_of)
        elif option == "3":
            print("\n[TODO] DFS ainda não implementado.")
        elif option == "0":
            print("\nEncerrando o programa.")
            break


# Requisito 2: Informações gerais do grafo
def print_graph_info(graph: Graph):
    """Exibe as informações gerais do grafo."""
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
    
    # Origem e Destino para o teste de falha
        # origin = "mary.miller@enron.com"
        # destination = "drew.fossum@enron.com"
def interactive_bfs(graph: Graph, index_of: dict[str, int]):
    """Loop interativo para testar alcançabilidade via BFS."""
    print(f"\nBusca em largura (BFS) — alcançabilidade entre dois indivíduos")
    print("Digite 'sair' para voltar ao menu.\n")

    while True:
        origin = get_valid_email(index_of, "Remetente (email): ")
        if origin is None:
            break

        destination = get_valid_email(index_of, "Destinatário (email): ")
        if destination is None:
            break

        graph.print_bfs_reach(index_of[origin], index_of[destination])
        print()