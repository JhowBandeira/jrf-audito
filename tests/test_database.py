import tempfile
import unittest
from pathlib import Path

from sqlalchemy import text

from backend.core.database import DATABASE_PATH, DATABASE_URL, SessionLocal, criar_engine


class TestDatabase(unittest.TestCase):
    def test_database_path_e_previsivel(self):
        self.assertEqual(DATABASE_PATH.name, "jrf_audito.db")
        self.assertIn("data", DATABASE_PATH.parts)
        self.assertIn("database", DATABASE_PATH.parts)
        self.assertTrue(DATABASE_URL.startswith("sqlite:///"))

    def test_cria_conexao_sqlite_temporaria(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "teste.db"
            engine = criar_engine(f"sqlite:///{caminho.as_posix()}")
            try:
                with engine.connect() as conexao:
                    resultado = conexao.execute(text("select 1")).scalar_one()

                self.assertEqual(resultado, 1)
            finally:
                engine.dispose()

    def test_session_local_existe(self):
        self.assertIsNotNone(SessionLocal)


if __name__ == "__main__":
    unittest.main()
