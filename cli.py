"""
Arquivo responsável pela interface interativa com o usuário.
"""
from graph_pkg import Graph
from cli_utils import get_valid_email, get_menu_option, ask_yes_no, save_result_log


def interactive_menu(graph: Graph, index_of: dict[str, int]):
    """Menu interativo principal do programa."""
    while True:
        print(f"\n{'='*50}")
        print("MENU PRINCIPAL")
        print(f"{'='*50}")
        print("1. Informações gerais do grafo")
        print("2. Busca em profundidade (DFS)")
        print("3. Busca em largura (BFS)")
        print("4. Nós a distância D de um vértice")
        print("5. Caminho crítico (Dijkstra)")
        print("0. Sair")
        print(f"{'='*50}")

        option: str = get_menu_option(["0", "1", "2", "3", "4", "5"])

        if option == "1":
            print_graph_info(graph)
        elif option == "2":
            print("\n[TODO] Requisito 3: DFS ainda não está implementado.")
        elif option == "3":
            interactive_bfs(graph, index_of)
        elif option == "4":
            print("\n[TODO] Requisito 5: Nós a distância D de um vértice ainda não está implementado.")
        elif option == "5":
            interactive_critical_path(graph, index_of)
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


# TODO: Requisito 3: Busca em profundidade (DFS) — alcançabilidade entre dois indivíduos


# Requisito 4: Busca em largura (BFS) — alcançabilidade entre dois indivíduos
def interactive_bfs(graph: Graph, index_of: dict[str, int]):
    """Loop interativo para testar alcançabilidade via BFS."""
    print(f"\nBusca em largura (BFS) — alcançabilidade entre dois indivíduos")
    print("Digite 'sair' para voltar ao menu.\n")

    while True:
        origin: str | None = get_valid_email(index_of, "Remetente (email): ")
        if origin is None:
            break

        destination: str | None = get_valid_email(index_of, "Destinatário (email): ")
        if destination is None:
            break

        reachable, visited = graph.print_bfs_reach(index_of[origin], index_of[destination])

        if reachable:
            if ask_yes_no("Deseja visualizar a lista de nós visitados? (s/n): "):
                for label in visited:
                    print(f"  {label}")

            if ask_yes_no("Deseja salvar o resultado em log? (s/n): "):
                content = f"BFS: {origin} → {destination}\n"
                content += f"Alcançável: Sim\n"
                content += f"Nós visitados ({len(visited)}):\n"
                for label in visited:
                    content += f"  {label}\n"
                save_result_log(content, "bfs_reach")
        else:
            if ask_yes_no("Deseja salvar o resultado em log? (s/n): "):
                content = f"BFS: {origin} → {destination}\n"
                content += f"Alcançável: Não\n"
                save_result_log(content, "bfs_reach")

        print()


# TODO: Requisito 5: Nós a distância D de um vértice

# Requisito 6: Caminho crítico (Dijkstra)
def interactive_critical_path(graph: Graph, index_of: dict[str, int]):
    """Loop interativo para encontrar o caminho crítico via Dijkstra."""
    print(f"\nCaminho crítico — Dijkstra com peso invertido")
    print("Digite 'sair' para voltar ao menu.\n")

    while True:
        origin: str | None = get_valid_email(index_of, "Origem (email): ")
        if origin is None:
            break

        destination: str | None = get_valid_email(index_of, "Destino (email): ")
        if destination is None:
            break

        graph.print_critical_path(index_of[origin], index_of[destination])

        if ask_yes_no("Deseja salvar o resultado em log? (s/n): "):
            distance, previous = graph.dijkstra_critical_path(index_of[origin])

            if distance[index_of[destination]] == float("inf"):
                content = f"Dijkstra: {origin} → {destination}\n"
                content += f"Alcançável: Não\n"
            else:
                path, accumulated_cost = graph.reconstruct_critical_path(
                    index_of[origin], index_of[destination], previous
                )
                content = f"Dijkstra: {origin} → {destination}\n"
                content += f"Caminho: {' → '.join(path)}\n"
                content += f"Dependência acumulada: {accumulated_cost}\n"

            save_result_log(content, "critical_path")

        print()
