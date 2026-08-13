# JRF-Audito

Backend em Python para organizar rotinas de auditoria e processamento fiscal com foco em empresas, participantes, inscricoes, regras fiscais e base para apuracao.

## Problema

Processos fiscais costumam ficar espalhados entre planilhas, arquivos XML, controles manuais e regras repetidas em varios lugares. Isso dificulta rastrear dados, validar cadastros, reaproveitar regras e evoluir o sistema com seguranca.

## Solucao

O JRF-Audito estrutura um backend fiscal modular, com API, modelos, schemas, repositories, services, migrations e testes. O projeto centraliza regras fiscais e cria uma base para importar, normalizar, validar e auditar informacoes fiscais sem misturar regra de negocio com interface.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- pandas
- openpyxl
- SQLite
- unittest / TestClient

## Funcionalidades presentes no codigo

- API FastAPI com rotas para empresas, inscricoes e participantes.
- Camadas separadas de models, schemas, repositories e services.
- Migrations com Alembic.
- Regras fiscais de CFOP organizadas em modulo proprio.
- Importador Excel inicial.
- Testes para API, models, repositories, services, banco e regras de CFOP.

## Estrutura

```text
backend/
  api/
  core/
  importadores/
  models/
  repositories/
  schemas/
  services/
  regras_fiscais/
alembic/
tests/
docs/
```

## Como executar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

## Testes

```bash
python -m unittest
```

## Observacao de seguranca

Dados reais, bancos locais, planilhas de empresas, arquivos importados e artefatos de ambiente foram removidos desta publicacao.
