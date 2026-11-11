import unittest
import pandas as pd

from src.clean_data import clean_data
from src.analyze_data import analyze_data

class TestSalesPipeline(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame([
            {"pedido_id": "P1", "data": "2026-01-01", "cliente_id": "C1",
             "produto": "Mouse", "categoria": "Acessórios", "regiao": "Sul",
             "quantidade": 2, "preco_unitario": 50.0},
            {"pedido_id": "P2", "data": "2026-01-02", "cliente_id": "C2",
             "produto": "Teclado", "categoria": "Acessórios", "regiao": "Sudeste",
             "quantidade": 1, "preco_unitario": 100.0},
            {"pedido_id": "P3", "data": "2026-01-03", "cliente_id": "C3",
             "produto": "Inválido", "categoria": "Teste", "regiao": "Sul",
             "quantidade": 0, "preco_unitario": 10.0},
        ])

    def test_clean_removes_invalid_rows(self):
        cleaned, stats = clean_data(self.data)
        self.assertEqual(len(cleaned), 2)
        self.assertEqual(stats["linhas_descartadas"], 1)
        self.assertAlmostEqual(cleaned["faturamento"].sum(), 200.0)

    def test_summary_revenue(self):
        cleaned, _ = clean_data(self.data)
        result = analyze_data(cleaned)
        self.assertAlmostEqual(result["resumo_geral"].iloc[0]["faturamento_total"], 200.0)
        self.assertEqual(result["resumo_geral"].iloc[0]["pedidos"], 2)

    def test_missing_required_column_raises(self):
        with self.assertRaises(ValueError):
            clean_data(pd.DataFrame({"pedido_id": ["P1"]}))

if __name__ == "__main__":
    unittest.main()
