# Enron Contact Analyzer

Analisador de rede de contatos baseado na base de dados de e-mails Enron. O projeto constrói um grafo direcionado e ponderado para representar as relações de comunicação entre usuários, permitindo análises de conectividade e alcançabilidade.

## Características

- **Carregamento de e-mails**: Lê e-mails da base de dados Enron
- **Análise de frequência**: Calcula a frequência de contatos entre pares de usuários
- **Construção de grafo**: Cria um grafo direcionado, ponderado e rotulado
- **Análise de graus**: Identifica os principais remetentes (saída) e destinatários (entrada)
- **Busca em profundidade (DFS)**: Próxima implementação
- **Busca em largura (BFS)**: Verifica alcançabilidade entre dois indivíduos
- **Nós a distância D de um vértice**: Próxima implementação
- **Caminho crítico (Dijkstra)**: Encontra o caminho de maior dependência acumulada entre dois indivíduos

## Estrutura do Projeto

```
enron_contact_analyzer/
├── config.py                 # Configurações e variáveis de ambiente
├── main.py                   # Ponto de entrada da aplicação
├── cli.py                    # Interface interativa (menu e loops de entrada)
├── cli_utils.py              # Funções auxiliares para validação de entrada
├── requirements.txt          # Dependências do projeto
├── env.example               # Exemplo de variáveis de ambiente
├── enron_pkg/                # Pacote para parsing de e-mails
│   ├── __init__.py
│   └── email_parser.py       # Classe Email e funções de carregamento
├── graph_pkg/                # Pacote com estruturas de grafo
│   ├── __init__.py
│   ├── graph.py              # Classe principal do grafo
│   └── linked_list.py        # Estrutura de lista encadeada para adjacências
└── logs/                     # Diretório para arquivos de log (gitignored)
```

## Estrutura Esperada do Dataset

O banco de dados Enron deve estar organizado da seguinte forma:

```
enron_mail_database/
├── usuario-a/
│   └── sent/
│       ├── 1
│       ├── 2
│       └── ...
├── usuario-b/
│   └── sent/
│       ├── 1
│       └── ...
└── ...
```

## Instalação

1. Clone o repositório
2. Configure suas variáveis de ambiente criando um arquivo `.env`:
   ```
   ENRON_DATABASE_PATH=./enron_mail_database
   SENT_FOLDER=sent
   LOG_DIR=logs
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Execute o programa principal:

```bash
python main.py
```

O programa irá:
1. Carregar todos os e-mails da pasta `sent` de cada usuário
2. Calcular a frequência de contatos entre pares de usuários
3. Construir o grafo com as relações identificadas
4. Exibir um menu interativo com as opções disponíveis

## Menu Interativo

```
==================================================
MENU PRINCIPAL
==================================================
1. Informações gerais do grafo
2. Busca em profundidade (DFS)
3. Busca em largura (BFS)
4. Nós a distância D de um vértice
5. Caminho crítico (Dijkstra)
0. Sair
==================================================
```

## Requisitos Implementados

- Construção do grafo direcionado, ponderado e rotulado
- Informações gerais do grafo (vértices, arestas, graus)
- Busca em largura (BFS) para alcançabilidade
- Caminho crítico via Dijkstra com peso invertido