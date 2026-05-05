# Enron Contact Analyzer

Analisador de rede de contatos baseado na base de dados de e-mails Enron. O projeto constrói um grafo direcionado e ponderado para representar as relações de comunicação entre usuários, permitindo análises de conectividade e alcançabilidade.

## Características

- **Carregamento de e-mails**: Lê e-mails da base de dados Enron
- **Análise de frequência**: Calcula a frequência de contatos entre pares de usuários
- **Construção de grafo**: Cria um grafo direcionado, ponderado e rotulado
- **Análise de graus**: Identifica os principais remetentes (saída) e destinatários (entrada)
- **Busca em profundidade (DFS)**: Verifica alcançabilidade entre dois indivíduos
- **Busca em largura (BFS)**: Verifica alcançabilidade entre dois indivíduos
- **Nós a distância D de um vértice**: Retorna os nós a uma distância exata de arestas
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
├── tests/                    # Scripts de diagnóstico e validação
│   ├── test_env_config.py    # Verifica variáveis de ambiente e caminhos
│   └── test_file_access.py   # Verifica acesso aos arquivos do dataset
├── cache/                    # Cache de dados processados (gitignored)
└── logs/                     # Diretório para arquivos de log (gitignored)
```

## Estrutura Esperada do Dataset

O dataset Enron é público e está disponível em: https://www.cs.cmu.edu/~enron/

O banco de dados deve estar organizado da seguinte forma:

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
   CACHE_DIR=cache
   CACHE_FILENAME=frequency.pkl
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
1. Carregar os dados (do cache ou processando os e-mails do dataset)
2. Construir o grafo com as relações identificadas
3. Exibir um menu interativo com as opções disponíveis

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

## Compatibilidade Windows

Ao extrair o dataset Enron (`tar.gz`) no Windows, os arquivos de e-mail podem ser criados com um ponto no final do nome (ex: `1.`, `2.`, `3.` ao invés de `1`, `2`, `3`). Isso é um artefato de como o Windows lida com arquivos sem extensão vindos de sistemas Unix.

O `email_parser.py` trata essa situação automaticamente usando o prefixo `\\?\` no caminho dos arquivos no Windows, que impede a normalização de nomes pelo sistema operacional. No Linux, o comportamento é transparente.

## Scripts de Diagnóstico

A pasta `tests/` contém scripts criados durante o desenvolvimento para diagnosticar problemas de compatibilidade entre Linux e Windows na leitura do dataset:

- **test_env_config.py**: Verifica se as variáveis de ambiente estão configuradas corretamente e se os caminhos do dataset são acessíveis.
- **test_file_access.py**: Verifica se os arquivos de e-mail dentro do dataset são reconhecidos pelo sistema operacional (identifica problemas como o ponto trailing no Windows).

Para executar:
```bash
python tests/test_env_config.py
python tests/test_file_access.py
```

## Projeto

PUCPR Grafos — Projeto Colaborativo 1

## Autores

- Angelo Piovezan
- Renato Gouveia