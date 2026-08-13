# CHANGELOG JRF-Audito

## 2026-08-10

### Fase 1.9 - Adicionado

- `backend/utils/documentos.py` para normalizacao compartilhada de CPF/CNPJ e tipo de pessoa.
- `backend/models/participante.py` com `Participante` e `ParticipantePapel`.
- `backend/repositories/participante_repository.py`.
- `backend/services/participante_service.py`.
- `backend/schemas/participante.py`.
- `backend/api/routes/participantes.py`.
- `alembic/versions/20260810_0003_criar_participantes.py`.
- `tests/test_participantes_models.py`.
- `tests/test_participante_repository.py`.
- `tests/test_participante_service.py`.
- `tests/test_participantes_api.py`.

### Fase 1.9 - Alterado

- `backend/models/empresa.py`: adicionado relacionamento 1:N com Participantes.
- `backend/models/__init__.py`: adicionados `Participante` e `ParticipantePapel`.
- `backend/services/empresa_service.py`: `normalizar_cnpj()` passou a reutilizar utilitario compartilhado de documentos.
- `backend/main.py`: registrado router de Participantes.
- `docs/HANDOFF.md`: atualizado com Fase 1.9.
- `docs/CHANGELOG.md`: atualizado com Fase 1.9.

### Fase 1.9 - Banco

- Criada tabela `participantes`.
- Criada tabela `participantes_papeis`.
- Criada foreign key `participantes.empresa_id -> empresas.id`.
- Criada foreign key `participantes_papeis.participante_id -> participantes.id`.
- Criada constraint unique `empresa_id + cpf_cnpj`.
- Criada constraint unique `participante_id + papel`.

### Fase 1.9 - Pendente

- Validacao matematica de CPF/CNPJ, se aprovada futuramente.
- Update/delete de Participante.
- Participantes sem CPF/CNPJ, se houver caso real futuro.
- Consulta Receita Federal ou fontes externas, somente em fase futura aprovada.
- Vinculo automatico de documentos fiscais com Participante.

## 2026-08-10

### Fase 1.8 - Adicionado

- `backend/utils/ufs.py` para normalizacao compartilhada de UF.
- `backend/models/inscricao_estadual.py`.
- `backend/models/inscricao_municipal.py`.
- `backend/repositories/inscricao_estadual_repository.py`.
- `backend/repositories/inscricao_municipal_repository.py`.
- `backend/services/inscricao_estadual_service.py`.
- `backend/services/inscricao_municipal_service.py`.
- `backend/schemas/inscricao_estadual.py`.
- `backend/schemas/inscricao_municipal.py`.
- `backend/api/routes/inscricoes_estaduais.py`.
- `backend/api/routes/inscricoes_municipais.py`.
- `alembic/versions/20260810_0002_criar_inscricoes_estaduais_e_municipais.py`.
- `tests/test_inscricoes_models.py`.
- `tests/test_inscricoes_repositories.py`.
- `tests/test_inscricoes_services.py`.
- `tests/test_inscricoes_api.py`.

### Fase 1.8 - Alterado

- `backend/models/empresa.py`: adicionados relacionamentos 1:N com IE e IM.
- `backend/models/__init__.py`: adicionados novos models.
- `backend/services/empresa_service.py`: UF passou a usar utilitario compartilhado.
- `backend/schemas/empresa.py`: UF passou a usar utilitario compartilhado.
- `backend/main.py`: registrados routers de IE e IM.
- `docs/HANDOFF.md`: atualizado com Fase 1.8.
- `docs/CHANGELOG.md`: atualizado com Fase 1.8.

### Fase 1.8 - Banco

- Criada tabela `inscricoes_estaduais`.
- Criada tabela `inscricoes_municipais`.
- Criadas foreign keys para `empresas.id`.
- Criadas constraints de unicidade para evitar duplicidades por empresa.

### Fase 1.8 - Pendente

- Update/delete de IE/IM.
- Validacoes fiscais de IE por UF.
- Normalizacao oficial de municipios.
- Consultas externas de IE/IM, somente em fase futura aprovada.
