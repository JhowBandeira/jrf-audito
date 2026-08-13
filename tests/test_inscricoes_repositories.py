import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.database import Base
from backend.models.empresa import Empresa
from backend.repositories.inscricao_estadual_repository import InscricaoEstadualRepository
from backend.repositories.inscricao_municipal_repository import InscricaoMunicipalRepository


class TestInscricoesRepositories(unittest.TestCase):
    def criar_sessao_temporaria(self):
        pasta = tempfile.TemporaryDirectory()
        caminho = Path(pasta.name) / "inscricoes_repository_teste.db"
        engine = create_engine(f"sqlite:///{caminho.as_posix()}")
        Base.metadata.create_all(bind=engine)
        Sessao = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        return pasta, engine, Sessao()

    def criar_empresa(self, sessao):
        empresa = Empresa(cnpj="12345678000199", razao_social="Empresa Repo Ltda")
        sessao.add(empresa)
        sessao.commit()
        return empresa

    def test_criar_e_listar_ie_por_empresa(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            empresa = self.criar_empresa(sessao)
            repo = InscricaoEstadualRepository(sessao)
            repo.criar_inscricao_estadual(
                empresa_id=empresa.id,
                uf="SP",
                inscricao_estadual="IE123",
            )

            inscricoes = repo.listar_por_empresa(empresa.id)

            self.assertEqual(len(inscricoes), 1)
            self.assertEqual(inscricoes[0].uf, "SP")
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_criar_e_listar_im_por_empresa(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            empresa = self.criar_empresa(sessao)
            repo = InscricaoMunicipalRepository(sessao)
            repo.criar_inscricao_municipal(
                empresa_id=empresa.id,
                municipio="Sao Paulo",
                uf="SP",
                inscricao_municipal="IM123",
            )

            inscricoes = repo.listar_por_empresa(empresa.id)

            self.assertEqual(len(inscricoes), 1)
            self.assertEqual(inscricoes[0].municipio, "Sao Paulo")
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()


if __name__ == "__main__":
    unittest.main()
