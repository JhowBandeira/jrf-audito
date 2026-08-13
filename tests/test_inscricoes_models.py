import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.database import Base
from backend.models.empresa import Empresa
from backend.models.inscricao_estadual import InscricaoEstadual
from backend.models.inscricao_municipal import InscricaoMunicipal


class TestInscricoesModels(unittest.TestCase):
    def criar_sessao_temporaria(self):
        pasta = tempfile.TemporaryDirectory()
        caminho = Path(pasta.name) / "inscricoes_model_teste.db"
        engine = create_engine(f"sqlite:///{caminho.as_posix()}")
        Base.metadata.create_all(bind=engine)
        Sessao = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        return pasta, engine, Sessao()

    def test_persistencia_e_relacionamento_com_empresa(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            empresa = Empresa(cnpj="12345678000199", razao_social="Empresa Model Ltda")
            sessao.add(empresa)
            sessao.commit()

            ie = InscricaoEstadual(
                empresa_id=empresa.id,
                uf="SP",
                inscricao_estadual="IE123",
                situacao="ativa",
            )
            im = InscricaoMunicipal(
                empresa_id=empresa.id,
                municipio="Sao Paulo",
                uf="SP",
                inscricao_municipal="IM123",
                situacao="ativa",
            )
            sessao.add_all([ie, im])
            sessao.commit()
            sessao.refresh(empresa)

            self.assertEqual(ie.empresa.cnpj, "12345678000199")
            self.assertEqual(im.empresa.cnpj, "12345678000199")
            self.assertEqual(len(empresa.inscricoes_estaduais), 1)
            self.assertEqual(len(empresa.inscricoes_municipais), 1)
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()


if __name__ == "__main__":
    unittest.main()
