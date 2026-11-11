import logging
import pandas as pd

from src.config import (
    RAW_FILE, CLEAN_FILE, DB_FILE, EXCEL_FILE, LOG_FILE,
    OUTPUT_CHARTS_DIR, OUTPUT_REPORTS_DIR, create_directories
)
from src.generate_data import generate_data
from src.clean_data import clean_data
from src.analyze_data import analyze_data
from src.database import save_to_sqlite, run_example_query
from src.charts import create_charts

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True,
    )

def run_pipeline():
    create_directories()
    setup_logging()
    logging.info("Iniciando pipeline de análise de vendas.")

    try:
        if not RAW_FILE.exists():
            logging.info("Arquivo bruto não encontrado; gerando dados fictícios.")
            generate_data()

        raw = pd.read_csv(RAW_FILE)
        logging.info("Dados brutos carregados: %s linhas.", len(raw))

        clean, cleaning_stats = clean_data(raw)
        if clean.empty:
            raise ValueError("A limpeza não deixou nenhum registro válido.")

        clean.to_csv(CLEAN_FILE, index=False, encoding="utf-8")
        logging.info(
            "Limpeza concluída: entrada=%s, válidas=%s, descartadas=%s.",
            cleaning_stats["linhas_entrada"],
            cleaning_stats["linhas_validas"],
            cleaning_stats["linhas_descartadas"],
        )

        analyses = analyze_data(clean)
        save_to_sqlite(clean, DB_FILE)
        create_charts(analyses, OUTPUT_CHARTS_DIR)

        OUTPUT_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        for name, table in analyses.items():
            table.to_csv(OUTPUT_REPORTS_DIR / f"{name}.csv", index=False, encoding="utf-8")

        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
            clean.to_excel(writer, sheet_name="Dados tratados", index=False)
            for name, table in analyses.items():
                table.to_excel(writer, sheet_name=name[:31], index=False)

        sql_result = run_example_query(DB_FILE)
        logging.info("Consulta SQL de exemplo:\n%s", sql_result.to_string(index=False))
        logging.info("Pipeline concluído com sucesso.")
        print("\nResumo geral:")
        print(analyses["resumo_geral"].to_string(index=False))
        print(f"\nRelatório Excel: {EXCEL_FILE}")
        print(f"Gráficos: {OUTPUT_CHARTS_DIR}")
        print(f"Banco SQLite: {DB_FILE}")
        return analyses
    except Exception:
        logging.exception("Falha durante a execução do pipeline.")
        raise

if __name__ == "__main__":
    run_pipeline()
