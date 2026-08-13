# HANDOFF JRF-Audito

Data: 2026-08-10
Etapa concluida: Fase 1.9 - Cadastro de Participantes

## Estado atual

Fases concluidas:

- Fase 1.1: fundacao documental/estrutural minima.
- Fase 1.2: limpeza dos prints manuais do CFOP e testes de CFOP.
- Fase 1.3: importador Excel reutilizavel.
- Fase 1.4: SQLAlchemy, Alembic, SQLite e model Empresa.
- Fase 1.5: repository e service de Empresa.
- Fase 1.6: FastAPI inicial e API de Empresas.
- Fase 1.7: validacoes cadastrais leves e erros simples padronizados.
- Fase 1.8: Inscricoes Estaduais e Municipais.
- Fase 1.9: cadastro central de Participantes com papeis multiplos.

## Estrutura relevante

- `backend/utils/documentos.py`: normalizacao compartilhada de CPF/CNPJ e tipo de pessoa.
- `backend/models/participante.py`: models `Participante` e `ParticipantePapel`.
- `backend/repositories/participante_repository.py`: repository de Participante.
- `backend/services/participante_service.py`: service de Participante.
- `backend/schemas/participante.py`: schemas HTTP de Participante.
- `backend/api/routes/participantes.py`: endpoints de Participante.
- `alembic/versions/20260810_0003_criar_participantes.py`: migration da Fase 1.9.

## Model

### Participante

Caminho: `backend/models/participante.py`

Campos:

- `id`
- `empresa_id`
- `tipo_pessoa`
- `cpf_cnpj`
- `razao_social_nome`
- `nome_fantasia`
- `inscricao_estadual`
- `inscricao_municipal`
- `email`
- `telefone`
- `cep`
- `logradouro`
- `numero`
- `complemento`
- `bairro`
- `municipio`
- `uf`
- `situacao`
- `criado_em`
- `atualizado_em`

### ParticipantePapel

Tabela simples para permitir mais de um papel por participante.

Campos:

- `id`
- `participante_id`
- `papel`
- `criado_em`

## Papeis

Papeis aceitos nesta fase:

- `cliente`
- `fornecedor`
- `prestador`
- `tomador`
- `transportadora`
- `outros`

O participante deve possuir pelo menos um papel.

## Relacionamentos

- Empresa 1:N Participantes.
- Participante 1:N ParticipantePapel.
- Cada Participante pertence a uma Empresa por `empresa_id`.
- O mesmo CPF/CNPJ pode existir em empresas diferentes, mas nao duplicado na mesma empresa.

## Banco / Migration

SQLite real:

```text
data/database/jrf_audito.db
```

Revision atual:

```text
20260810_0003
```

Migration criada:

```text
alembic/versions/20260810_0003_criar_participantes.py
```

Tabelas criadas:

- `participantes`
- `participantes_papeis`

Foreign keys:

- `participantes.empresa_id -> empresas.id`
- `participantes_papeis.participante_id -> participantes.id`

Constraints:

- `uq_participantes_empresa_cpf_cnpj`: unique em `empresa_id + cpf_cnpj`.
- `uq_participantes_papeis_participante_papel`: unique em `participante_id + papel`.

Indices:

- `participantes`: `id`, `empresa_id`, `cpf_cnpj`, `razao_social_nome`, `uf`.
- `participantes_papeis`: `id`, `participante_id`, `papel`.

## Repository

Caminho: `backend/repositories/participante_repository.py`

Funcoes:

- `criar_participante(papeis, **dados)`
- `buscar_por_id(empresa_id, participante_id)`
- `buscar_por_cpf_cnpj(empresa_id, cpf_cnpj)`
- `listar_por_empresa(empresa_id)`
- `buscar_duplicado(empresa_id, cpf_cnpj)`

O repository nao executa commit.

## Service

Caminho: `backend/services/participante_service.py`

Responsabilidades:

- validar Empresa existente.
- normalizar `tipo_pessoa` como `PF` ou `PJ`.
- normalizar CPF/CNPJ removendo pontuacao.
- validar CPF com 11 digitos e CNPJ com 14 digitos.
- normalizar `razao_social_nome`.
- normalizar e validar papeis.
- normalizar UF com `backend/utils/ufs.py`.
- impedir duplicidade por `empresa_id + cpf_cnpj`.
- coordenar commit/rollback.

Excecoes:

- `ParticipanteDadosInvalidosError`
- `ParticipanteJaExisteError`
- `ParticipanteNaoEncontradoError`
- reutiliza `EmpresaNaoEncontradaError`

## Schemas

Caminho: `backend/schemas/participante.py`

- `TipoPessoa`: enum `PF`/`PJ`.
- `PapelParticipante`: enum dos papeis permitidos.
- `ParticipanteCreate`: payload de criacao.
- `ParticipanteResponse`: resposta da API, com `papeis` como lista de strings.

## Endpoints

- `POST /empresas/{empresa_id}/participantes`
- `GET /empresas/{empresa_id}/participantes`
- `GET /empresas/{empresa_id}/participantes/{participante_id}`
- `GET /empresas/{empresa_id}/participantes/documento/{cpf_cnpj}`

Erros:

- Empresa inexistente: `404`.
- Participante inexistente: `404`.
- Participante duplicado: `409`.
- Payload invalido: `422`.

## Testes

Novos testes:

- `tests/test_participantes_models.py`
- `tests/test_participante_repository.py`
- `tests/test_participante_service.py`
- `tests/test_participantes_api.py`

Cenarios cobertos:

- persistencia e vinculo com Empresa.
- criacao, busca e listagem no repository.
- isolamento de participantes por empresa.
- empresa inexistente.
- participante inexistente.
- duplicidade.
- normalizacao de CPF/CNPJ, tipo de pessoa, razao social/nome, papeis e UF.
- POST/GET via API.
- 404, 409 e 422 via API.

## Como rodar os testes

```text
$env:PYTHONPATH=(Get-Location); .\.venv\Scripts\python.exe -m unittest tests.test_database tests.test_empresa_model tests.test_importador_excel tests.test_regras_cfop tests.test_empresa_repository tests.test_empresa_service tests.test_empresas_api tests.test_inscricoes_models tests.test_inscricoes_repositories tests.test_inscricoes_services tests.test_inscricoes_api tests.test_participantes_models tests.test_participante_repository tests.test_participante_service tests.test_participantes_api
```

Resultado da ultima execucao:

```text
Ran 68 tests in 9.871s
OK
```

## Como aplicar migrations

```text
$env:PYTHONPATH=(Get-Location); .\.venv\Scripts\alembic.exe upgrade head
```

## Como iniciar API

```text
$env:PYTHONPATH=(Get-Location); .\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

## Decisoes de arquitetura

- Participante e o cadastro central de terceiros.
- Cliente, fornecedor, prestador, tomador e transportadora sao papeis, nao tabelas separadas.
- Papeis ficam em tabela relacionada para permitir mais de um papel e expansao futura.
- `empresa_id + cpf_cnpj` evita duplicidade dentro da mesma Empresa.
- CPF/CNPJ usa validacao estrutural simples, sem consulta externa e sem validacao matematica nesta fase.
- Endereco permanece no proprio Participante.
- Municipio permanece texto livre.
- UF reutiliza utilitario compartilhado.

## Pendencias

- Validacao matematica de CPF/CNPJ, se aprovada futuramente.
- Participantes sem CPF/CNPJ, se houver caso real futuro.
- Update/delete de Participante.
- Consulta Receita Federal ou fontes externas, somente em fase aprovada.
- Normalizacao oficial de municipio/IBGE.
- Vinculo automatico de NF-e/NFS-e/CT-e com Participante.

## Problemas conhecidos

- Nao ha validacao externa de CPF/CNPJ.
- Nao ha validacao matematica de digitos verificadores.
- Email e telefone ainda sao strings simples.
- Nao ha cadastro estruturado de endereco.

## Proximo passo recomendado

Fase 1.10: criar update/delete controlado para cadastros existentes ou iniciar relacionamento de documentos fiscais com Participante, somente apos aprovacao.
