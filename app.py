"""
Interface web do Enron Contact Analyzer usando Streamlit.
Execução: streamlit run app.py
"""

import os
import pickle
import streamlit as st
from config import ENRON_DATABASE_PATH, SENT_FOLDER, LOG_DIR, CACHE_PATH, CACHE_DIR
from enron_pkg import load_emails, get_unique_addresses
from graph_pkg import Graph


# ─────────────────────────────────────────────
# Carregamento e construção do grafo (com cache)
# ─────────────────────────────────────────────

@st.cache_data
def load_data():
    """Carrega frequências do cache ou faz o parsing dos emails."""
    if os.path.isfile(CACHE_PATH):
        with open(CACHE_PATH, "rb") as file:
            return pickle.load(file)

    frequency = load_emails(ENRON_DATABASE_PATH, sent_folder=SENT_FOLDER, log_dir=LOG_DIR)

    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_PATH, "wb") as file:
        pickle.dump(frequency, file)

    return frequency


@st.cache_resource
def build_graph(_frequency):
    """Constrói o grafo a partir do dicionário de frequências."""
    addresses = get_unique_addresses(_frequency)
    index_of = {address: index for index, address in enumerate(addresses)}

    graph = Graph(len(addresses))
    for index, address in enumerate(addresses):
        graph.update_information(index, address)
    for (sender, recipient), weight in _frequency.items():
        graph.create_adjacency(index_of[sender], index_of[recipient], weight)

    return graph, index_of, addresses


# ─────────────────────────────────────────────
# Páginas
# ─────────────────────────────────────────────

def page_general_info(graph, frequency):
    """Página de informações gerais do grafo."""
    st.header("Informações Gerais do Grafo")

    col1, col2, col3 = st.columns(3)
    col1.metric("Vértices", f"{graph.size:,}")
    col2.metric("Arestas", f"{graph.edge_count():,}")
    col3.metric("Total de mensagens", f"{sum(frequency.values()):,}")

    col_out, col_in = st.columns(2)

    with col_out:
        st.subheader("Top 20 — Grau de Saída")
        for rank, (label, degree) in enumerate(graph.top_out_degree(20), 1):
            st.text(f"{rank:>2}. {label}: {degree}")

    with col_in:
        st.subheader("Top 20 — Grau de Entrada")
        for rank, (label, degree) in enumerate(graph.top_in_degree(20), 1):
            st.text(f"{rank:>2}. {label}: {degree}")


def page_bfs(graph, index_of, addresses):
    """Página de busca em largura (BFS)."""
    st.header("Busca em Largura (BFS)")
    st.write("Verifica se um indivíduo pode alcançar outro através da rede de contatos.")

    col1, col2 = st.columns(2)
    with col1:
        origin = st.selectbox("Origem", addresses, key="bfs_origin")
    with col2:
        destination = st.selectbox("Destino", addresses, key="bfs_dest")

    if st.button("Buscar via BFS", type="primary"):
        if origin == destination:
            st.warning("Origem e destino são o mesmo endereço.")
            return

        reachable, visited = graph.bfs_reach(index_of[origin], index_of[destination])

        if reachable:
            st.success(f"**{origin}** alcança **{destination}** via BFS.")
            st.info(f"Nós visitados: **{len(visited)}**")

            with st.expander("Ver lista de nós visitados"):
                for index, label in enumerate(visited, 1):
                    st.text(f"{index:>4}. {label}")
        else:
            st.error(f"**{origin}** NÃO alcança **{destination}** via BFS.")


def page_dfs(graph, index_of, addresses):
    """Página de busca em profundidade (DFS)."""
    st.header("Busca em Profundidade (DFS)")
    st.write("Verifica se um indivíduo pode alcançar outro através da rede de contatos.")

    col1, col2 = st.columns(2)
    with col1:
        origin = st.selectbox("Origem", addresses, key="dfs_origin")
    with col2:
        destination = st.selectbox("Destino", addresses, key="dfs_dest")

    if st.button("Buscar via DFS", type="primary"):
        if origin == destination:
            st.warning("Origem e destino são o mesmo endereço.")
            return

        reachable, visited = graph.dfs_reach(index_of[origin], index_of[destination])

        if reachable:
            st.success(f"**{origin}** alcança **{destination}** via DFS.")
            st.info(f"Nós visitados: **{len(visited)}**")

            with st.expander("Ver lista de nós visitados"):
                for index, label in enumerate(visited, 1):
                    st.text(f"{index:>4}. {label}")
        else:
            st.error(f"**{origin}** NÃO alcança **{destination}** via DFS.")


def page_distance_d(graph, index_of, addresses):
    """Página de nós a distância D."""
    st.header("Nós a Distância D")
    st.write("Distância 1 = destinatários diretos, 2 = destinatários dos destinatários, etc.")

    col1, col2 = st.columns(2)
    with col1:
        origin = st.selectbox("Nó origem", addresses, key="dist_origin")
    with col2:
        distance = st.number_input("Distância (D)", min_value=0, max_value=20, value=1)

    if st.button("Buscar", type="primary"):
        nodes = graph.nodes_at_distance(index_of[origin], distance)

        if nodes:
            st.success(f"Encontrados **{len(nodes)}** nós a distância **{distance}** de **{origin}**.")

            with st.expander("Ver nós encontrados"):
                for index, node in enumerate(nodes, 1):
                    st.text(f"{index:>4}. {node}")
        else:
            st.warning(f"Nenhum nó encontrado a distância {distance} de {origin}.")


def page_critical_path(graph, index_of, addresses):
    """Página do caminho crítico via Dijkstra."""
    st.header("Caminho Crítico (Dijkstra)")
    st.write("Encontra o caminho de maior dependência acumulada usando peso invertido (1/peso).")

    col1, col2 = st.columns(2)
    with col1:
        origin = st.selectbox("Origem", addresses, key="dijk_origin")
    with col2:
        destination = st.selectbox("Destino", addresses, key="dijk_dest")

    if st.button("Encontrar caminho crítico", type="primary"):
        if origin == destination:
            st.warning("Origem e destino são o mesmo endereço.")
            return

        distance, previous = graph.dijkstra_critical_path(index_of[origin])

        if distance[index_of[destination]] == float("inf"):
            st.error(f"**{origin}** NÃO alcança **{destination}**.")
            return

        path, accumulated_cost = graph.reconstruct_critical_path(
            index_of[origin], index_of[destination], previous
        )

        st.success(f"Caminho encontrado com dependência acumulada de **{accumulated_cost}**.")

        st.subheader("Caminho")
        st.write(" → ".join(path))

        st.subheader("Detalhes")
        for index, node in enumerate(path, 1):
            st.text(f"{index:>2}. {node}")


def page_top_pairs(frequency):
    """Página com os pares de maior frequência."""
    st.header("Pares com Mais Mensagens")

    amount = st.slider("Quantidade", min_value=5, max_value=50, value=10)

    top_pairs = sorted(frequency.items(), key=lambda item: item[1], reverse=True)[:amount]

    for rank, ((sender, recipient), count) in enumerate(top_pairs, 1):
        st.text(f"{rank:>3}. {sender} → {recipient}: {count} mensagem(ns)")


# ─────────────────────────────────────────────
# App principal
# ─────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="Enron Contact Analyzer",
        page_icon="📧",
        layout="wide",
    )

    st.title("📧 Enron Contact Analyzer")

    with st.spinner("Carregando dados..."):
        frequency = load_data()
        graph, index_of, addresses = build_graph(frequency)

    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Escolha uma opção:", [
        "Informações gerais",
        "Busca em largura (BFS)",
        "Busca em profundidade (DFS)",
        "Nós a distância D",
        "Caminho crítico (Dijkstra)",
        "Top pares de mensagens",
    ])

    if page == "Informações gerais":
        page_general_info(graph, frequency)
    elif page == "Busca em largura (BFS)":
        page_bfs(graph, index_of, addresses)
    elif page == "Busca em profundidade (DFS)":
        page_dfs(graph, index_of, addresses)
    elif page == "Nós a distância D":
        page_distance_d(graph, index_of, addresses)
    elif page == "Caminho crítico (Dijkstra)":
        page_critical_path(graph, index_of, addresses)
    elif page == "Top pares de mensagens":
        page_top_pairs(frequency)

    st.sidebar.divider()
    st.sidebar.caption("PUCPR Grafos — Projeto Colaborativo 1")
    st.sidebar.caption("Angelo Piovezan & Renato Gouveia")


if __name__ == "__main__":
    main()