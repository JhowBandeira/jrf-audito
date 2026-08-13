import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.database import Base
from backend.services.empresa_service import (
    EmpresaDadosInvalidosError,
    EmpresaJaExisteError,
    EmpresaNaoEncontradaError,
    EmpresaService,
    normalizar_cnpj,
    validar_cnpj,
)


class TestEmpresaService(unittest.TestCase):
    def criar_sessao_temporaria(self):
        pasta = tempfile.TemporaryDirectory()
        caminho = Path(pasta.name) / "service_teste.db"
        engine = create_engine(f"sqlite:///{caminho.as_posix()}")
        Base.metadata.create_all(bind=engine)
        Sessao = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        return pasta, engine, Sessao()

    def test_cadastrar_empresa(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            service = EmpresaService(sessao)
            empresa = service.criar_empresa(
                cnpj="12.345.678/0001-99",
                razao_social="  Empresa Service Ltda  ",
                tipo_estabelecimento="matriz",
                uf="sp",
            )

            self.assertIsNotNone(empresa.id)
            self.assertEqual(empresa.cnpj, "12345678000199")
            self.assertEqual(empresa.razao_social, "Empresa Service Ltda")
            self.assertEqual(empresa.tipo_estabelecimento, "matriz")
            self.assertEqual(empresa.uf, "SP")
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_impede_cnpj_duplicado_de_forma_controlada(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            service = EmpresaService(sessao)
            service.criar_empresa(cnpj="12.345.678/0001-99", razao_social="Empresa A")

            with self.assertRaises(EmpresaJaExisteError):
                service.criar_empresa(cnpj="12345678000199", razao_social="Empresa B")
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_normalizar_cnpj(self):
        self.assertEqual(normalizar_cnpj("12.345.678/0001-99"), "12345678000199")
        self.assertEqual(normalizar_cnpj("  12345678000199  "), "12345678000199")

    def test_validar_cnpj_sem_mascara(self):
        self.assertEqual(validar_cnpj("12345678000199"), "12345678000199")

    def test_validar_cnpj_curto_longo_e_vazio(self):
        for cnpj in ("123", "123456780001999", "", "../"):
            with self.assertRaises(EmpresaDadosInvalidosError):
                validar_cnpj(cnpj)

    def test_buscar_empresa_por_cnpj_normaliza_entrada(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            service = EmpresaService(sessao)
            service.criar_empresa(cnpj="12345678000199", razao_social="Empresa Service Ltda")

            encontrada = service.buscar_empresa_por_cnpj("12.345.678/0001-99")

            self.assertEqual(encontrada.razao_social, "Empresa Service Ltda")
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_razao_social_vazia(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            service = EmpresaService(sessao)
            with self.assertRaises(EmpresaDadosInvalidosError):
                service.criar_empresa(cnpj="12345678000199", razao_social="   ")
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_tipo_estabelecimento_invalido(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            service = EmpresaService(sessao)
            with self.assertRaises(EmpresaDadosInvalidosError):
                service.criar_empresa(
                    cnpj="12345678000199",
                    razao_social="Empresa Service Ltda",
                    tipo_estabelecimento="deposito",
                )
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_uf_invalida(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            service = EmpresaService(sessao)
            with self.assertRaises(EmpresaDadosInvalidosError):
                service.criar_empresa(
                    cnpj="12345678000199",
                    razao_social="Empresa Service Ltda",
                    uf="XX",
                )
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()

    def test_empresa_nao_encontrada(self):
        pasta, engine, sessao = self.criar_sessao_temporaria()
        try:
            service = EmpresaService(sessao)
            with self.assertRaises(EmpresaNaoEncontradaError):
                service.obter_empresa_por_id(999)
        finally:
            sessao.close()
            engine.dispose()
            pasta.cleanup()


if __name__ == "__main__":
    unittest.main()
