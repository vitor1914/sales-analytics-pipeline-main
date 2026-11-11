import pandas as pd

def analyze_data(df):
    """Retorna tabelas de indicadores e análises para relatórios."""
    if df.empty:
        raise ValueError("Não há dados válidos para analisar.")

    data = df.copy()
    data["data"] = pd.to_datetime(data["data"], errors="raise")
    total_revenue = round(float(data["faturamento"].sum()), 2)
    order_count = int(data["pedido_id"].nunique())
    total_units = int(data["quantidade"].sum())

    summary = pd.DataFrame([{
        "faturamento_total": total_revenue,
        "pedidos": order_count,
        "unidades_vendidas": total_units,
        "clientes_unicos": int(data["cliente_id"].nunique()),
        "ticket_medio": round(total_revenue / order_count, 2) if order_count else 0,
        "produto_mais_vendido": str(data.groupby("produto")["quantidade"].sum().idxmax()),
        "regiao_maior_faturamento": str(data.groupby("regiao")["faturamento"].sum().idxmax()),
    }])

    data["mes"] = data["data"].dt.to_period("M").astype(str)
    monthly = data.groupby("mes", as_index=False).agg(
        faturamento=("faturamento", "sum"),
        pedidos=("pedido_id", "nunique"),
        unidades=("quantidade", "sum"),
    )
    monthly["faturamento"] = monthly["faturamento"].round(2)

    products = data.groupby(["produto", "categoria"], as_index=False).agg(
        faturamento=("faturamento", "sum"),
        unidades=("quantidade", "sum"),
        pedidos=("pedido_id", "nunique"),
    ).sort_values("faturamento", ascending=False)
    products["faturamento"] = products["faturamento"].round(2)

    regions = data.groupby("regiao", as_index=False).agg(
        faturamento=("faturamento", "sum"),
        pedidos=("pedido_id", "nunique"),
        unidades=("quantidade", "sum"),
    ).sort_values("faturamento", ascending=False)
    regions["faturamento"] = regions["faturamento"].round(2)

    categories = data.groupby("categoria", as_index=False).agg(
        faturamento=("faturamento", "sum"),
        unidades=("quantidade", "sum"),
    ).sort_values("faturamento", ascending=False)
    categories["faturamento"] = categories["faturamento"].round(2)

    return {
        "resumo_geral": summary,
        "vendas_mensais": monthly,
        "vendas_produto": products,
        "vendas_regiao": regions,
        "vendas_categoria": categories,
    }
