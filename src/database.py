import sqlite3
import pandas as pd

def save_to_sqlite(df, db_path):
    """Grava os dados tratados em SQLite, substituindo a tabela de destino."""
    with sqlite3.connect(db_path) as connection:
        df.to_sql("vendas", connection, if_exists="replace", index=False)
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_vendas_data ON vendas(data)
        """)
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_vendas_produto ON vendas(produto)
        """)
        connection.commit()

def run_example_query(db_path):
    """Executa uma consulta SQL demonstrativa e devolve o resultado."""
    query = """
        SELECT produto,
               SUM(quantidade) AS unidades_vendidas,
               ROUND(SUM(faturamento), 2) AS faturamento
        FROM vendas
        GROUP BY produto
        ORDER BY faturamento DESC
    """
    with sqlite3.connect(db_path) as connection:
        return pd.read_sql_query(query, connection)
