import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.database import Base
from backend.models.empresa import Empresa
from backend.repositories.participante_repository import ParticipanteRepository


class TestParticipanteRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.SessionTeste = sessionmaker(bind=self.engine)
        self.sessao = self.SessionTeste()
        self.repository = ParticipanteRepository(self.sessao)

    def tearDown(self):
        self.sessao.close()
        Base.metadata.drop_all(bind=self.engine)
        self.engine.dispose()

    def criar_empresa(self, cnpj="12345678000199"):
        empresa = Empresa(cnpj=cnpj, razao_social="Empresa Teste")
        self.sessao.add(empresa)
        self.sessao.commit()
        return empresa

    def criar_participante(self, empresa_id):
        participante = self.repository.criar_participante(
            empresa_id=empresa_id,
            tipo_pessoa="PJ",
            cpf_cnpj="11222333000181",
            razao_social_nome="Fornecedor Teste Ltda",
            papeis=["fornecedor"],
        )
        self.sessao.commit()
        return participante

    def test_criar_buscar_e_listar_por_empresa(self):
        empresa = self.criar_empresa()
        participante = self.criar_participante(empresa.id)

        por_id = self.repository.buscar_por_id(empresa.id, participante.id)
        por_documento = self.repository.buscar_por_cpf_cnpj(empresa.id, "11222333000181")
        lista = self.repository.listar_por_empresa(empresa.id)

        self.assertEqual(por_id.id, participante.id)
        self.assertEqual(por_documento.id, participante.id)
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0].papeis[0].papel, "fornecedor")

    def test_listar_nao_mistura_empresas(self):
        empresa_a = self.criar_empresa("12345678000199")
        empresa_b = self.criar_empresa("98765432000188")
        self.criar_participante(empresa_a.id)

        self.assertEqual(len(self.repository.listar_por_empresa(empresa_a.id)), 1)
        self.assertEqual(len(self.repository.listar_por_empresa(empresa_b.id)), 0)


if __name__ == "__main__":
    unittest.main()
