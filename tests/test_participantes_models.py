import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.database import Base
from backend.models.empresa import Empresa
from backend.models.participante import Participante, ParticipantePapel


class TestParticipantesModels(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.SessionTeste = sessionmaker(bind=self.engine)
        self.sessao = self.SessionTeste()

    def tearDown(self):
        self.sessao.close()
        Base.metadata.drop_all(bind=self.engine)
        self.engine.dispose()

    def criar_empresa(self):
        empresa = Empresa(cnpj="12345678000199", razao_social="Empresa Teste")
        self.sessao.add(empresa)
        self.sessao.commit()
        return empresa

    def test_persiste_participante_com_papeis(self):
        empresa = self.criar_empresa()
        participante = Participante(
            empresa_id=empresa.id,
            tipo_pessoa="PJ",
            cpf_cnpj="11222333000181",
            razao_social_nome="Fornecedor Teste Ltda",
            uf="SP",
        )
        participante.papeis = [ParticipantePapel(papel="cliente"), ParticipantePapel(papel="fornecedor")]

        self.sessao.add(participante)
        self.sessao.commit()
        self.sessao.refresh(participante)

        self.assertIsNotNone(participante.id)
        self.assertEqual(participante.empresa_id, empresa.id)
        self.assertEqual(participante.empresa.id, empresa.id)
        self.assertEqual({papel.papel for papel in participante.papeis}, {"cliente", "fornecedor"})


if __name__ == "__main__":
    unittest.main()
