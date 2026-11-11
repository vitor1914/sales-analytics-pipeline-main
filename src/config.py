from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_RAW_DIR = ROOT_DIR / "data" / "raw"
DATA_PROCESSED_DIR = ROOT_DIR / "data" / "processed"
OUTPUT_CHARTS_DIR = ROOT_DIR / "outputs" / "charts"
OUTPUT_REPORTS_DIR = ROOT_DIR / "outputs" / "reports"
LOG_DIR = ROOT_DIR / "logs"

RAW_FILE = DATA_RAW_DIR / "vendas.csv"
CLEAN_FILE = DATA_PROCESSED_DIR / "vendas_tratadas.csv"
DB_FILE = DATA_PROCESSED_DIR / "vendas.db"
EXCEL_FILE = OUTPUT_REPORTS_DIR / "analise_vendas.xlsx"
LOG_FILE = LOG_DIR / "pipeline.log"

REQUIRED_COLUMNS = [
    "pedido_id", "data", "cliente_id", "produto", "categoria",
    "regiao", "quantidade", "preco_unitario"
]

def create_directories():
    for path in (
        DATA_RAW_DIR, DATA_PROCESSED_DIR, OUTPUT_CHARTS_DIR,
        OUTPUT_REPORTS_DIR, LOG_DIR
    ):
        path.mkdir(parents=True, exist_ok=True)
