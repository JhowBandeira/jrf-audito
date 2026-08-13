import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.database import Base
from backend.models.empresa import Empresa
from backend.services.empresa_service import EmpresaNaoEncontradaError
from backend.services.participante_service import (
    ParticipanteDadosInvalidosError,
    ParticipanteJaExisteError,
    ParticipanteNaoEncontradoError,
    ParticipanteService,
)


class TestParticipanteService(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.SessionTeste = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        self.sessao = self.SessionTeste()
        self.service = ParticipanteService(self.sessao)

    def tearDown(self):
        self.sessao.close()
        Base.metadata.drop_all(bind=self.engine)
        self.engine.dispose()

    def criar_empresa(self):
        empresa = Empresa(cnpj="12345678000199", razao_social="Empresa Teste")
        self.sessao.add(empresa)
        self.sessao.commit()
        return empresa

    def payload(self, **extras):
        dados = {
            "tipo_pessoa": "PJ",
            "cpf_cnpj": "11.222.333/0001-81",
            "razao_social_nome": " Fornecedor Teste Ltda ",
            "papeis": ["fornecedor", "cliente"],
            "uf": "sp",
        }
        dados.update(extras)
        return dados

    def test_cria_participante_normalizando_documento_texto_papeis_e_uf(self):
        empresa = self.criar_empresa()

        participante = self.service.criar_participante(empresa_id=empresa.id, **self.payload())

        self.assertEqual(participante.tipo_pessoa, "PJ")
        self.assertEqual(participante.cpf_cnpj, "11222333000181")
        self.assertEqual(participante.razao_social_nome, "Fornecedor Teste Ltda")
        self.assertEqual(participante.uf, "SP")
        self.assertEqual([papel.papel for papel in participante.papeis], ["fornecedor", "cliente"])

    def test_cria_participante_pf(self):
        empresa = self.criar_empresa()

        participante = self.service.criar_participante(
            empresa_id=empresa.id,
            **self.payload(tipo_pessoa="pf", cpf_cnpj="123.456.789-01", razao_social_nome="Pessoa Fisica"),
        )

        self.assertEqual(participante.tipo_pessoa, "PF")
        self.assertEqual(participante.cpf_cnpj, "12345678901")

    def test_empresa_inexistente(self):
        with self.assertRaises(EmpresaNaoEncontradaError):
            self.service.criar_participante(empresa_id=999, **self.payload())

    def test_duplicidade(self):
        empresa = self.criar_empresa()
        self.service.criar_participante(empresa_id=empresa.id, **self.payload())

        with self.assertRaises(ParticipanteJaExisteError):
            self.service.criar_participante(empresa_id=empresa.id, **self.payload())

    def test_tipo_pessoa_invalido(self):
        empresa = self.criar_empresa()

        with self.assertRaises(ParticipanteDadosInvalidosError):
            self.service.criar_participante(empresa_id=empresa.id, **self.payload(tipo_pessoa="MEI"))

    def test_uf_invalida(self):
        empresa = self.criar_empresa()

        with self.assertRaises(ParticipanteDadosInvalidosError):
            self.service.criar_participante(empresa_id=empresa.id, **self.payload(uf="XX"))

    def test_participante_inexistente(self):
        empresa = self.criar_empresa()

        with self.assertRaises(ParticipanteNaoEncontradoError):
            self.service.obter_por_id(empresa.id, 999)


if __name__ == "__main__":
    unittest.main()
