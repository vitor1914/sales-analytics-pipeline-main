import pandas as pd
from src.config import REQUIRED_COLUMNS

def clean_data(df):
    """Valida o esquema, remove duplicatas e descarta registros inválidos."""
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing_columns}")

    data = df[REQUIRED_COLUMNS].copy()
    input_rows = len(data)
    data = data.drop_duplicates()

    for col in ["pedido_id", "cliente_id", "produto", "categoria", "regiao"]:
        data[col] = data[col].astype("string").str.strip()

    data["data"] = pd.to_datetime(data["data"], errors="coerce")
    data["quantidade"] = pd.to_numeric(data["quantidade"], errors="coerce")
    data["preco_unitario"] = pd.to_numeric(data["preco_unitario"], errors="coerce")

    essential = ["pedido_id", "data", "cliente_id", "produto", "categoria", "regiao",
                 "quantidade", "preco_unitario"]
    data = data.dropna(subset=essential)
    data = data[
        (data["quantidade"] > 0)
        & (data["preco_unitario"] > 0)
        & (data["quantidade"] % 1 == 0)
    ].copy()

    data["quantidade"] = data["quantidade"].astype(int)
    data["preco_unitario"] = data["preco_unitario"].round(2)
    data["faturamento"] = (data["quantidade"] * data["preco_unitario"]).round(2)
    data["data"] = data["data"].dt.strftime("%Y-%m-%d")
    data = data.sort_values(["data", "pedido_id"]).reset_index(drop=True)

    stats = {
        "linhas_entrada": input_rows,
        "linhas_validas": len(data),
        "linhas_descartadas": input_rows - len(data),
    }
    return data, stats
