import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from backend.core.database import Base
from backend.models.empresa import Empresa


class TestEmpresaModel(unittest.TestCase):
    def criar_sessao_temporaria(self):
        pasta = tempfile.TemporaryDirectory()
        caminho = Path(pasta.name) / "empresa_teste.db"
        engine = create_engine(f"sqlite:///{caminho.as_posix()}")
        Base.metadata.create_all(bind=engine)
        Sessao = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        return pasta, engine, Sessao()

    def test_empresa_pode_ser_persistida_e_consultada(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            empresa = Empresa(
                cnpj="12345678000199",
                razao_social="Empresa Teste Ltda",
                nome_fantasia="Empresa Teste",
                cnpj_raiz="12345678",
                tipo_estabelecimento="matriz",
                regime_tributario="simples_nacional",
                cnae_principal="6201501",
                municipio="Sao Paulo",
                uf="SP",
                situacao="ativa",
            )

            sessao.add(empresa)
            sessao.commit()

            encontrada = sessao.execute(
                select(Empresa).where(Empresa.cnpj == "12345678000199")
            ).scalar_one()

            self.assertEqual(encontrada.razao_social, "Empresa Teste Ltda")
            self.assertEqual(encontrada.tipo_estabelecimento, "matriz")
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_cnpj_unico(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            primeira = Empresa(cnpj="12345678000199", razao_social="Empresa A")
            segunda = Empresa(cnpj="12345678000199", razao_social="Empresa B")

            sessao.add(primeira)
            sessao.commit()
            sessao.add(segunda)

            with self.assertRaises(IntegrityError):
                sessao.commit()
        finally:
            sessao.rollback()
            sessao.close()
            engine.dispose()
            pasta.cleanup()


if __name__ == "__main__":
    unittest.main()
