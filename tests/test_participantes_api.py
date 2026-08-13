import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.api.dependencies import obter_sessao_api
from backend.core.database import Base
from backend.main import app


class TestParticipantesApi(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=self.engine)
        self.SessionTeste = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

        def obter_sessao_teste():
            sessao = self.SessionTeste()
            try:
                yield sessao
            finally:
                sessao.close()

        app.dependency_overrides[obter_sessao_api] = obter_sessao_teste
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=self.engine)
        self.engine.dispose()

    def criar_empresa(self):
        resposta = self.client.post(
            "/empresas",
            json={"cnpj": "12345678000199", "razao_social": "Empresa API Ltda"},
        )
        self.assertEqual(resposta.status_code, 201)
        return resposta.json()

    def payload(self, **extras):
        dados = {
            "tipo_pessoa": "PJ",
            "cpf_cnpj": "11.222.333/0001-81",
            "razao_social_nome": " Participante API Ltda ",
            "nome_fantasia": "Participante API",
            "papeis": ["cliente", "fornecedor"],
            "municipio": "Sao Paulo",
            "uf": "sp",
        }
        dados.update(extras)
        return dados

    def test_post_get_lista_get_id_e_get_documento(self):
        empresa = self.criar_empresa()
        resposta = self.client.post(f"/empresas/{empresa['id']}/participantes", json=self.payload())

        self.assertEqual(resposta.status_code, 201)
        dados = resposta.json()
        self.assertEqual(dados["empresa_id"], empresa["id"])
        self.assertEqual(dados["cpf_cnpj"], "11222333000181")
        self.assertEqual(dados["razao_social_nome"], "Participante API Ltda")
        self.assertEqual(dados["uf"], "SP")
        self.assertEqual(dados["papeis"], ["cliente", "fornecedor"])

        lista = self.client.get(f"/empresas/{empresa['id']}/participantes")
        self.assertEqual(lista.status_code, 200)
        self.assertEqual(len(lista.json()), 1)

        por_id = self.client.get(f"/empresas/{empresa['id']}/participantes/{dados['id']}")
        self.assertEqual(por_id.status_code, 200)
        self.assertEqual(por_id.json()["id"], dados["id"])

        por_documento = self.client.get(f"/empresas/{empresa['id']}/participantes/documento/11.222.333%2F0001-81")
        self.assertEqual(por_documento.status_code, 200)
        self.assertEqual(por_documento.json()["id"], dados["id"])

    def test_empresa_inexistente_retorna_404(self):
        resposta = self.client.post("/empresas/999/participantes", json=self.payload())

        self.assertEqual(resposta.status_code, 404)

    def test_participante_inexistente_retorna_404(self):
        empresa = self.criar_empresa()

        resposta = self.client.get(f"/empresas/{empresa['id']}/participantes/999")

        self.assertEqual(resposta.status_code, 404)

    def test_duplicidade_retorna_409(self):
        empresa = self.criar_empresa()
        self.client.post(f"/empresas/{empresa['id']}/participantes", json=self.payload())

        resposta = self.client.post(f"/empresas/{empresa['id']}/participantes", json=self.payload())

        self.assertEqual(resposta.status_code, 409)

    def test_payload_invalido_retorna_422(self):
        empresa = self.criar_empresa()

        resposta = self.client.post(
            f"/empresas/{empresa['id']}/participantes",
            json=self.payload(tipo_pessoa="PJ", cpf_cnpj="123", papeis=["cliente"]),
        )

        self.assertEqual(resposta.status_code, 422)

    def test_papel_invalido_retorna_422(self):
        empresa = self.criar_empresa()

        resposta = self.client.post(
            f"/empresas/{empresa['id']}/participantes",
            json=self.payload(papeis=["comprador"]),
        )

        self.assertEqual(resposta.status_code, 422)


if __name__ == "__main__":
    unittest.main()
