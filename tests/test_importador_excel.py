import tempfile
import unittest
from pathlib import Path

import pandas as pd

from backend.importadores.importador_excel import importar_excel


class TestImportadorExcel(unittest.TestCase):
    def test_le_excel_valido_e_retorna_dataframe(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "arquivo.xlsx"
            pd.DataFrame({"codigo": [1], "valor": [10.5]}).to_excel(caminho, index=False)

            tabela = importar_excel(caminho)

            self.assertIsInstance(tabela, pd.DataFrame)
            self.assertEqual(list(tabela.columns), ["codigo", "valor"])
            self.assertEqual(tabela.loc[0, "codigo"], 1)

    def test_header_configuravel(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "arquivo_com_cabecalho_na_terceira_linha.xlsx"
            pd.DataFrame(
                [
                    ["linha ignorada", ""],
                    ["outra linha ignorada", ""],
                    ["codigo", "valor"],
                    [101, 20.75],
                ]
            ).to_excel(caminho, index=False, header=False)

            tabela = importar_excel(caminho, header=2)

            self.assertEqual(list(tabela.columns), ["codigo", "valor"])
            self.assertEqual(tabela.loc[0, "codigo"], 101)

    def test_arquivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            importar_excel("arquivo_que_nao_existe.xlsx")

    def test_extensao_incompativel(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "arquivo.txt"
            caminho.write_text("conteudo", encoding="utf-8")

            with self.assertRaises(ValueError):
                importar_excel(caminho)


if __name__ == "__main__":
    unittest.main()
