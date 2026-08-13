import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.database import Base
from backend.services.empresa_service import EmpresaNaoEncontradaError, EmpresaService
from backend.services.inscricao_estadual_service import (
    InscricaoEstadualDadosInvalidosError,
    InscricaoEstadualJaExisteError,
    InscricaoEstadualService,
)
from backend.services.inscricao_municipal_service import (
    InscricaoMunicipalDadosInvalidosError,
    InscricaoMunicipalJaExisteError,
    InscricaoMunicipalService,
)


class TestInscricoesServices(unittest.TestCase):
    def criar_sessao_temporaria(self):
        pasta = tempfile.TemporaryDirectory()
        caminho = Path(pasta.name) / "inscricoes_service_teste.db"
        engine = create_engine(f"sqlite:///{caminho.as_posix()}")
        Base.metadata.create_all(bind=engine)
        Sessao = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        return pasta, engine, Sessao()

    def criar_empresa(self, sessao):
        return EmpresaService(sessao).criar_empresa(
            cnpj="12345678000199",
            razao_social="Empresa Service Ltda",
        )

    def test_criar_ie_normaliza_uf(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            empresa = self.criar_empresa(sessao)
            service = InscricaoEstadualService(sessao)
            inscricao = service.criar_inscricao_estadual(
                empresa_id=empresa.id,
                uf="sp",
                inscricao_estadual="  IE123  ",
            )

            self.assertEqual(inscricao.uf, "SP")
            self.assertEqual(inscricao.inscricao_estadual, "IE123")
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_ie_empresa_inexistente_e_duplicidade(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            service = InscricaoEstadualService(sessao)
            with self.assertRaises(EmpresaNaoEncontradaError):
                service.criar_inscricao_estadual(
                    empresa_id=999,
                    uf="SP",
                    inscricao_estadual="IE123",
                )

            empresa = self.criar_empresa(sessao)
            service.criar_inscricao_estadual(
                empresa_id=empresa.id,
                uf="SP",
                inscricao_estadual="IE123",
            )
            with self.assertRaises(InscricaoEstadualJaExisteError):
                service.criar_inscricao_estadual(
                    empresa_id=empresa.id,
                    uf="sp",
                    inscricao_estadual="IE123",
                )
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_ie_dados_invalidos(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            empresa = self.criar_empresa(sessao)
            service = InscricaoEstadualService(sessao)
            with self.assertRaises(InscricaoEstadualDadosInvalidosError):
                service.criar_inscricao_estadual(
                    empresa_id=empresa.id,
                    uf="XX",
                    inscricao_estadual="IE123",
                )
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_criar_im_normaliza_dados(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            empresa = self.criar_empresa(sessao)
            service = InscricaoMunicipalService(sessao)
            inscricao = service.criar_inscricao_municipal(
                empresa_id=empresa.id,
                municipio="  Sao Paulo  ",
                uf="sp",
                inscricao_municipal="  IM123  ",
            )

            self.assertEqual(inscricao.municipio, "Sao Paulo")
            self.assertEqual(inscricao.uf, "SP")
            self.assertEqual(inscricao.inscricao_municipal, "IM123")
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_im_empresa_inexistente_e_duplicidade(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            service = InscricaoMunicipalService(sessao)
            with self.assertRaises(EmpresaNaoEncontradaError):
                service.criar_inscricao_municipal(
                    empresa_id=999,
                    municipio="Sao Paulo",
                    uf="SP",
                    inscricao_municipal="IM123",
                )

            empresa = self.criar_empresa(sessao)
            service.criar_inscricao_municipal(
                empresa_id=empresa.id,
                municipio="Sao Paulo",
                uf="SP",
                inscricao_municipal="IM123",
            )
            with self.assertRaises(InscricaoMunicipalJaExisteError):
                service.criar_inscricao_municipal(
                    empresa_id=empresa.id,
                    municipio="Sao Paulo",
                    uf="sp",
                    inscricao_municipal="IM123",
                )
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_im_dados_invalidos(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            empresa = self.criar_empresa(sessao)
            service = InscricaoMunicipalService(sessao)
            with self.assertRaises(InscricaoMunicipalDadosInvalidosError):
                service.criar_inscricao_municipal(
                    empresa_id=empresa.id,
                    municipio="   ",
                    uf="SP",
                    inscricao_municipal="IM123",
                )
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()


if __name__ == "__main__":
    unittest.main()
