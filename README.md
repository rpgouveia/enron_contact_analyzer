# Enron Contact Analyzer

Analisador de rede de contatos baseado na base de dados de e-mails Enron. O projeto constrói um grafo direcionado e ponderado para representar as relações de comunicação entre usuários, permitindo análises de conectividade e alcançabilidade.

## Características

- **Carregamento de e-mails**: Lê e-mails da base de dados Enron
- **Análise de frequência**: Calcula a frequência de contatos entre pares de usuários
- **Construção de grafo**: Cria um grafo direcionado, ponderado e rotulado
- **Análise de graus**: Identifica os principais remetentes (saída) e destinatários (entrada)
- **Busca em largura (BFS)**: Verifica alcançabilidade entre dois indivíduos
- **Busca em profundidade (DFS)**: Próxima implementação

## Estrutura do Projeto

```
enron_contact_analyzer/
├── config.py                 # Configurações e variáveis de ambiente
├── main.py                   # Ponto de entrada da aplicação
├── requirements.txt          # Dependências do projeto
├── enron_pkg/                # Pacote para parsing de e-mails
│   ├── __init__.py
│   └── email_parser.py       # Funções de carregamento e análise de e-mails
├── graph_pkg/                # Pacote com estruturas de grafo
│   ├── __init__.py
│   ├── graph.py              # Classe principal do grafo
│   └── linked_list.py        # Estrutura de lista encadeada para adjacências
└── logs/                     # Diretório para arquivos de log
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
4. Exibir estatísticas gerais do grafo
5. Realizar busca de alcançabilidade usando BFS

## Requisitos Implementados

- Construção do grafo direcionado, ponderado e rotulado
- Informações gerais do grafo (vértices, arestas, graus)
- Busca em largura (BFS) para alcançabilidade

