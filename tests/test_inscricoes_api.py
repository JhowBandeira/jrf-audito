import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.api.dependencies import obter_sessao_api
from backend.core.database import Base
from backend.main import app


class TestInscricoesApi(unittest.TestCase):
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

    def test_post_e_get_inscricao_estadual(self):
        empresa = self.criar_empresa()
        resposta = self.client.post(
            f"/empresas/{empresa['id']}/inscricoes-estaduais",
            json={
                "uf": "sp",
                "inscricao_estadual": " IE123 ",
                "situacao": "ativa",
                "data_inicio": "2026-01-01",
            },
        )

        self.assertEqual(resposta.status_code, 201)
        dados = resposta.json()
        self.assertEqual(dados["empresa_id"], empresa["id"])
        self.assertEqual(dados["uf"], "SP")
        self.assertEqual(dados["inscricao_estadual"], "IE123")

        lista = self.client.get(f"/empresas/{empresa['id']}/inscricoes-estaduais")
        self.assertEqual(lista.status_code, 200)
        self.assertEqual(len(lista.json()), 1)

    def test_post_e_get_inscricao_municipal(self):
        empresa = self.criar_empresa()
        resposta = self.client.post(
            f"/empresas/{empresa['id']}/inscricoes-municipais",
            json={
                "municipio": " Sao Paulo ",
                "uf": "sp",
                "inscricao_municipal": " IM123 ",
                "situacao": "ativa",
                "data_inicio": "2026-01-01",
            },
        )

        self.assertEqual(resposta.status_code, 201)
        dados = resposta.json()
        self.assertEqual(dados["empresa_id"], empresa["id"])
        self.assertEqual(dados["municipio"], "Sao Paulo")
        self.assertEqual(dados["uf"], "SP")
        self.assertEqual(dados["inscricao_municipal"], "IM123")

        lista = self.client.get(f"/empresas/{empresa['id']}/inscricoes-municipais")
        self.assertEqual(lista.status_code, 200)
        self.assertEqual(len(lista.json()), 1)

    def test_empresa_inexistente_retorna_404(self):
        ie = self.client.post(
            "/empresas/999/inscricoes-estaduais",
            json={"uf": "SP", "inscricao_estadual": "IE123"},
        )
        im = self.client.post(
            "/empresas/999/inscricoes-municipais",
            json={"municipio": "Sao Paulo", "uf": "SP", "inscricao_municipal": "IM123"},
        )

        self.assertEqual(ie.status_code, 404)
        self.assertEqual(im.status_code, 404)

    def test_duplicidade_retorna_409(self):
        empresa = self.criar_empresa()
        payload_ie = {"uf": "SP", "inscricao_estadual": "IE123"}
        payload_im = {"municipio": "Sao Paulo", "uf": "SP", "inscricao_municipal": "IM123"}

        self.client.post(f"/empresas/{empresa['id']}/inscricoes-estaduais", json=payload_ie)
        self.client.post(f"/empresas/{empresa['id']}/inscricoes-municipais", json=payload_im)

        ie = self.client.post(f"/empresas/{empresa['id']}/inscricoes-estaduais", json=payload_ie)
        im = self.client.post(f"/empresas/{empresa['id']}/inscricoes-municipais", json=payload_im)

        self.assertEqual(ie.status_code, 409)
        self.assertEqual(im.status_code, 409)


if __name__ == "__main__":
    unittest.main()
