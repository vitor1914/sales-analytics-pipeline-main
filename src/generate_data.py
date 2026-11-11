import random
from datetime import date, timedelta
import pandas as pd
from src.config import RAW_FILE, create_directories

PRODUCTS = [
    ("Notebook", "Eletrônicos", 3200.00),
    ("Mouse", "Acessórios", 75.00),
    ("Teclado", "Acessórios", 140.00),
    ("Monitor", "Eletrônicos", 950.00),
    ("Cadeira", "Móveis", 780.00),
    ("Headset", "Acessórios", 210.00),
    ("Webcam", "Eletrônicos", 260.00),
    ("Mesa", "Móveis", 650.00),
]
REGIONS = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

def generate_data(n_rows=1000, seed=42, include_quality_issues=True):
    """Gera vendas fictícias reproduzíveis para desenvolver e testar o pipeline."""
    random.seed(seed)
    today = date.today()
    start = today - timedelta(days=364)
    rows = []

    for i in range(1, n_rows + 1):
        product, category, price = random.choice(PRODUCTS)
        order_date = start + timedelta(days=random.randint(0, 364))
        quantity = random.randint(1, 5)
        row = {
            "pedido_id": f"P{i:06d}",
            "data": order_date.isoformat(),
            "cliente_id": f"C{random.randint(1, max(50, n_rows // 4)):05d}",
            "produto": product,
            "categoria": category,
            "regiao": random.choice(REGIONS),
            "quantidade": quantity,
            "preco_unitario": round(price * random.uniform(0.9, 1.1), 2),
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    if include_quality_issues and len(df) >= 10:
        df = pd.concat([df, df.iloc[[0]]], ignore_index=True)  # duplicata intencional
        df.loc[2, "quantidade"] = 0                           # inválido intencional
        df.loc[4, "produto"] = None                           # campo ausente intencional

    create_directories()
    df.to_csv(RAW_FILE, index=False, encoding="utf-8")
    print(f"Base fictícia salva em: {RAW_FILE} ({len(df)} linhas)")
    return df

if __name__ == "__main__":
    generate_data()
