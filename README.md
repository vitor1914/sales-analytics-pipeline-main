# Sales Analytics Pipeline

Projeto de portfólio para praticar Python, Pandas, SQL/SQLite, visualização de dados, Excel, logging e testes automatizados.

## Funcionalidades
- Geração de dados fictícios e reproduzíveis.
- Validação e limpeza de registros.
- Métricas de faturamento, unidades e ticket médio.
- Análises por mês, produto, categoria e região.
- Persistência em SQLite.
- Exportação de CSV, Excel e gráficos PNG.
- Logs da execução e testes com `unittest`.

## Tecnologias
Python 3.10+, pandas, matplotlib, openpyxl, SQLite e unittest.

## Estrutura
```text
sales-analytics-pipeline/
├── data/
│   ├── raw/.gitkeep
│   └── processed/.gitkeep
├── outputs/
│   ├── charts/.gitkeep
│   └── reports/.gitkeep
├── logs/.gitkeep
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── analyze_data.py
│   ├── database.py
│   ├── charts.py
│   └── pipeline.py
├── tests/
│   └── test_pipeline.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Instalação

### Linux / Ubuntu
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Executar o projeto
Na pasta raiz do projeto:
```bash
python -m src.pipeline
```

Por padrão, a execução cria dados fictícios se `data/raw/vendas.csv` não existir. Para gerar uma nova base fictícia:
```bash
python -m src.generate_data
```

## Testes
```bash
python -m unittest discover -s tests -v
```

## Principais saídas
- `data/raw/vendas.csv`: base bruta de exemplo.
- `data/processed/vendas_tratadas.csv`: dados validados.
- `outputs/reports/resumo_geral.csv`: indicadores gerais.
- `outputs/reports/analise_vendas.xlsx`: relatório com várias abas.
- `outputs/charts/`: gráficos PNG.
- `data/processed/vendas.db`: banco SQLite.
- `logs/pipeline.log`: histórico da execução.

## Regras de negócio
- `faturamento = quantidade * preco_unitario`
- `ticket médio = faturamento total / número de pedidos`
- Registros com campos essenciais ausentes, quantidade/preço não positivos ou datas inválidas são descartados.
- Duplicatas exatas são removidas.
- Os dados são fictícios e não representam uma empresa real.

## Sugestão de commits diários
1. Estrutura inicial e documentação.
2. Gerador de dados fictícios.
3. Validação de colunas e tipos.
4. Remoção de duplicatas e registros inválidos.
5. Métricas gerais.
6. Análise mensal.
7. Análise por produto e categoria.
8. Banco SQLite.
9. Exportação Excel.
10. Gráficos.
11. Logging e tratamento de exceções.
12. Testes automatizados.
13. Refatoração e documentação dos resultados.

## Licença
MIT
