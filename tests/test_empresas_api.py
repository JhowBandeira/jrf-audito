import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.api.dependencies import obter_sessao_api
from backend.core.database import Base
from backend.main import app


class TestEmpresasApi(unittest.TestCase):
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

    def test_health_check(self):
        resposta = self.client.get("/health")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json(), {"status": "ok"})

    def test_criar_empresa(self):
        resposta = self.client.post(
            "/empresas",
            json={
                "cnpj": "12.345.678/0001-99",
                "razao_social": "  Empresa API Ltda  ",
                "tipo_estabelecimento": "matriz",
                "uf": "sp",
            },
        )

        self.assertEqual(resposta.status_code, 201)
        dados = resposta.json()
        self.assertEqual(dados["cnpj"], "12345678000199")
        self.assertEqual(dados["razao_social"], "Empresa API Ltda")
        self.assertEqual(dados["tipo_estabelecimento"], "matriz")
        self.assertEqual(dados["uf"], "SP")
        self.assertIn("id", dados)

    def test_criar_empresa_com_cnpj_sem_mascara(self):
        resposta = self.client.post(
            "/empresas",
            json={"cnpj": "12345678000199", "razao_social": "Empresa API Ltda"},
        )

        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.json()["cnpj"], "12345678000199")

    def test_listar_empresas(self):
        self.client.post("/empresas", json={"cnpj": "11111111000111", "razao_social": "A Empresa"})
        self.client.post("/empresas", json={"cnpj": "22222222000122", "razao_social": "B Empresa"})

        resposta = self.client.get("/empresas")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.json()), 2)

    def test_buscar_empresa_por_id(self):
        criada = self.client.post(
            "/empresas",
            json={"cnpj": "12345678000199", "razao_social": "Empresa API Ltda"},
        ).json()

        resposta = self.client.get(f"/empresas/{criada['id']}")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["cnpj"], "12345678000199")

    def test_buscar_empresa_por_cnpj(self):
        self.client.post(
            "/empresas",
            json={"cnpj": "12345678000199", "razao_social": "Empresa API Ltda"},
        )

        resposta = self.client.get("/empresas/cnpj/12.345.678.0001-99")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["razao_social"], "Empresa API Ltda")

    def test_cnpj_duplicado_retorna_409(self):
        self.client.post("/empresas", json={"cnpj": "12345678000199", "razao_social": "Empresa A"})

        resposta = self.client.post(
            "/empresas",
            json={"cnpj": "12.345.678/0001-99", "razao_social": "Empresa B"},
        )

        self.assertEqual(resposta.status_code, 409)
        self.assertIn("ja cadastrada", resposta.json()["detail"])

    def test_cnpj_curto_longo_e_vazio_retornam_422(self):
        for cnpj in ("123", "123456780001999", ""):
            resposta = self.client.post(
                "/empresas",
                json={"cnpj": cnpj, "razao_social": "Empresa API Ltda"},
            )
            self.assertEqual(resposta.status_code, 422)

    def test_razao_social_vazia_retorna_422(self):
        resposta = self.client.post(
            "/empresas",
            json={"cnpj": "12345678000199", "razao_social": "   "},
        )

        self.assertEqual(resposta.status_code, 422)

    def test_tipo_estabelecimento_invalido_retorna_422(self):
        resposta = self.client.post(
            "/empresas",
            json={
                "cnpj": "12345678000199",
                "razao_social": "Empresa API Ltda",
                "tipo_estabelecimento": "deposito",
            },
        )

        self.assertEqual(resposta.status_code, 422)

    def test_uf_invalida_retorna_422(self):
        resposta = self.client.post(
            "/empresas",
            json={"cnpj": "12345678000199", "razao_social": "Empresa API Ltda", "uf": "XX"},
        )

        self.assertEqual(resposta.status_code, 422)

    def test_empresa_inexistente_por_id_retorna_404(self):
        resposta = self.client.get("/empresas/999")

        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(resposta.json(), {"detail": "Empresa nao encontrada."})

    def test_empresa_inexistente_por_cnpj_retorna_404(self):
        resposta = self.client.get("/empresas/cnpj/00000000000000")

        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(resposta.json(), {"detail": "Empresa nao encontrada."})


if __name__ == "__main__":
    unittest.main()
