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
            interactive_dfs(graph, index_of)
        elif option == "3":
            interactive_bfs(graph, index_of)
        elif option == "4":
            interactive_distance_d(graph, index_of)
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


# Requisito 3: Busca em profundidade (DFS) — alcançabilidade entre dois indivíduos
def interactive_dfs(graph: Graph, index_of: dict[str, int]):
    """Loop interativo para testar alcançabilidade via DFS."""
    print(f"\nBusca em profundidade (DFS) — alcançabilidade entre dois indivíduos")
    print("Digite 'sair' para voltar ao menu.\n")

    while True:
        origin: str | None = get_valid_email(index_of, "Remetente (email): ")
        if origin is None:
            break

        destination: str | None = get_valid_email(index_of, "Destinatário (email): ")
        if destination is None:
            break

        reachable, visited = graph.print_dfs_reach(index_of[origin], index_of[destination])

        if reachable:
            if ask_yes_no("Deseja visualizar a lista de nós visitados? (s/n): "):
                for label in visited:
                    print(f"  {label}")

            if ask_yes_no("Deseja salvar o resultado em log? (s/n): "):
                content = f"DFS: {origin} → {destination}\n"
                content += f"Alcançável: Sim\n"
                content += f"Nós visitados ({len(visited)}):\n"
                for label in visited:
                    content += f"  {label}\n"
                save_result_log(content, "dfs_reach")
        else:
            if ask_yes_no("Deseja salvar o resultado em log? (s/n): "):
                content = f"DFS: {origin} → {destination}\n"
                content += f"Alcançável: Não\n"
                save_result_log(content, "dfs_reach")
        print()


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


# Requisito 5: Nós a distância D de um vértice
def interactive_distance_d(graph: Graph, index_of: dict[str, int]):
    """Loop interativo para buscar nós a uma distância D."""
    print(f"\nNós a uma distância exata D de um vértice")
    print("Digite 'sair' no email para voltar ao menu.\n")

    while True:
        origin: str | None = get_valid_email(index_of, "Nó origem (email): ")
        if origin is None:
            break

        while True:
            distance_str = input("Distância (D): ").strip()
            if distance_str.isdigit():
                break
            print("  Distância inválida. Digite um número inteiro.\n")

        distance = int(distance_str)
        nodes = graph.nodes_at_distance(index_of[origin], distance)
        print(f"\nEncontrados {len(nodes)} nós a uma distância de {distance} aresta(s) de {origin}.")

        if nodes and ask_yes_no("Deseja visualizar os nós encontrados? (s/n): "):
            for node in nodes:
                print(f"  {node}")

        if ask_yes_no("Deseja salvar o resultado em log? (s/n): "):
            content = f"Origem: {origin}\n"
            content += f"Distância: {distance}\n"
            content += f"Nós encontrados ({len(nodes)}):\n"
            for node in nodes:
                content += f"  {node}\n"
            save_result_log(content, "distance_d")
        print()


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

        path, accumulated_cost = graph.print_critical_path(index_of[origin], index_of[destination])

        if path and ask_yes_no("Deseja salvar o resultado em log? (s/n): "):
            content = f"Dijkstra: {origin} → {destination}\n"
            content += f"Caminho: {' → '.join(path)}\n"
            content += f"Dependência acumulada: {accumulated_cost}\n"
            save_result_log(content, "critical_path")

        print()