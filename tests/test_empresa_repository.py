import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.database import Base
from backend.repositories.empresa_repository import EmpresaRepository


class TestEmpresaRepository(unittest.TestCase):
    def criar_sessao_temporaria(self):
        pasta = tempfile.TemporaryDirectory()
        caminho = Path(pasta.name) / "repository_teste.db"
        engine = create_engine(f"sqlite:///{caminho.as_posix()}")
        Base.metadata.create_all(bind=engine)
        Sessao = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        return pasta, engine, Sessao()

    def test_criar_empresa(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            repository = EmpresaRepository(sessao)
            empresa = repository.criar_empresa(
                cnpj="12345678000199",
                razao_social="Empresa Repository Ltda",
            )

            self.assertIsNotNone(empresa.id)
            self.assertEqual(empresa.cnpj, "12345678000199")
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_buscar_empresa_por_id(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            repository = EmpresaRepository(sessao)
            empresa = repository.criar_empresa(
                cnpj="12345678000199",
                razao_social="Empresa Repository Ltda",
            )
            encontrada = repository.buscar_empresa_por_id(empresa.id)

            self.assertEqual(encontrada.cnpj, "12345678000199")
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_buscar_empresa_por_cnpj(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            repository = EmpresaRepository(sessao)
            repository.criar_empresa(
                cnpj="12345678000199",
                razao_social="Empresa Repository Ltda",
            )
            encontrada = repository.buscar_empresa_por_cnpj("12345678000199")

            self.assertEqual(encontrada.razao_social, "Empresa Repository Ltda")
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_listar_empresas(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            repository = EmpresaRepository(sessao)
            repository.criar_empresa(cnpj="22222222000122", razao_social="B Empresa")
            repository.criar_empresa(cnpj="11111111000111", razao_social="A Empresa")

            empresas = repository.listar_empresas()

            self.assertEqual([empresa.razao_social for empresa in empresas], ["A Empresa", "B Empresa"])
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()


if __name__ == "__main__":
    unittest.main()
