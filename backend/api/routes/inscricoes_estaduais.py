"""Rotas HTTP de inscricoes estaduais."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.dependencies import obter_sessao_api
from backend.schemas.inscricao_estadual import (
    InscricaoEstadualCreate,
    InscricaoEstadualResponse,
)
from backend.services.empresa_service import EmpresaNaoEncontradaError
from backend.services.inscricao_estadual_service import (
    InscricaoEstadualDadosInvalidosError,
    InscricaoEstadualJaExisteError,
    InscricaoEstadualService,
)

router = APIRouter(prefix="/empresas/{empresa_id}/inscricoes-estaduais", tags=["inscricoes estaduais"])


def erro_http(status_code: int, mensagem: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail=mensagem)


@router.post("", response_model=InscricaoEstadualResponse, status_code=status.HTTP_201_CREATED)
def criar_inscricao_estadual(
    empresa_id: int,
    dados: InscricaoEstadualCreate,
    sessao: Session = Depends(obter_sessao_api),
) -> InscricaoEstadualResponse:
    service = InscricaoEstadualService(sessao)
    try:
        return service.criar_inscricao_estadual(empresa_id=empresa_id, **dados.model_dump())
    except EmpresaNaoEncontradaError as erro:
        raise erro_http(status.HTTP_404_NOT_FOUND, str(erro)) from erro
    except InscricaoEstadualJaExisteError as erro:
        raise erro_http(status.HTTP_409_CONFLICT, str(erro)) from erro
    except InscricaoEstadualDadosInvalidosError as erro:
        raise erro_http(status.HTTP_422_UNPROCESSABLE_ENTITY, str(erro)) from erro


@router.get("", response_model=list[InscricaoEstadualResponse])
def listar_inscricoes_estaduais(
    empresa_id: int,
    sessao: Session = Depends(obter_sessao_api),
) -> list[InscricaoEstadualResponse]:
    service = InscricaoEstadualService(sessao)
    try:
        return service.listar_por_empresa(empresa_id)
    except EmpresaNaoEncontradaError as erro:
        raise erro_http(status.HTTP_404_NOT_FOUND, str(erro)) from erro
