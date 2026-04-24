"""
Arquivo responsável pela interface interativa com o usuário.
"""
from graph_pkg import Graph


def interactive_bfs(graph: Graph, index_of: dict[str, int]):
    """Loop interativo para testar alcançabilidade via BFS."""
    print(f"\nBusca em largura (BFS) — alcançabilidade entre dois indivíduos")
    print("Digite 'sair' para encerrar.\n")

    while True:
        origin = ""
        while origin not in index_of:
            origin = input("Remetente (email): ").strip().lower()
            if origin == "sair":
                break
            if origin not in index_of:
                print(f"  Endereço '{origin}' não encontrado no grafo. Tente novamente.\n")

        if origin == "sair":
            break

        destination = ""
        while destination not in index_of:
            destination = input("Destinatário (email): ").strip().lower()
            if destination == "sair":
                break
            if destination not in index_of:
                print(f"  Endereço '{destination}' não encontrado no grafo. Tente novamente.\n")

        if destination == "sair":
            break

        graph.print_bfs_reach(index_of[origin], index_of[destination])
        print()

