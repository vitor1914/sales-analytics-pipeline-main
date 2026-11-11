import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def create_charts(analyses, output_dir):
    """Salva gráficos de faturamento mensal, por produto e por região."""
    output_dir.mkdir(parents=True, exist_ok=True)

    monthly = analyses["vendas_mensais"]
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(monthly["mes"], monthly["faturamento"], marker="o")
    ax.set_title("Faturamento mensal")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Faturamento (R$)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "faturamento_mensal.png", dpi=150)
    plt.close(fig)

    products = analyses["vendas_produto"].sort_values("faturamento")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(products["produto"], products["faturamento"])
    ax.set_title("Faturamento por produto")
    ax.set_xlabel("Faturamento (R$)")
    fig.tight_layout()
    fig.savefig(output_dir / "faturamento_produto.png", dpi=150)
    plt.close(fig)

    regions = analyses["vendas_regiao"].sort_values("faturamento")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(regions["regiao"], regions["faturamento"])
    ax.set_title("Faturamento por região")
    ax.set_xlabel("Região")
    ax.set_ylabel("Faturamento (R$)")
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(output_dir / "faturamento_regiao.png", dpi=150)
    plt.close(fig)
