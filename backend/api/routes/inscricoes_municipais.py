"""Rotas HTTP de inscricoes municipais."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.dependencies import obter_sessao_api
from backend.schemas.inscricao_municipal import (
    InscricaoMunicipalCreate,
    InscricaoMunicipalResponse,
)
from backend.services.empresa_service import EmpresaNaoEncontradaError
from backend.services.inscricao_municipal_service import (
    InscricaoMunicipalDadosInvalidosError,
    InscricaoMunicipalJaExisteError,
    InscricaoMunicipalService,
)

router = APIRouter(prefix="/empresas/{empresa_id}/inscricoes-municipais", tags=["inscricoes municipais"])


def erro_http(status_code: int, mensagem: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail=mensagem)


@router.post("", response_model=InscricaoMunicipalResponse, status_code=status.HTTP_201_CREATED)
def criar_inscricao_municipal(
    empresa_id: int,
    dados: InscricaoMunicipalCreate,
    sessao: Session = Depends(obter_sessao_api),
) -> InscricaoMunicipalResponse:
    service = InscricaoMunicipalService(sessao)
    try:
        return service.criar_inscricao_municipal(empresa_id=empresa_id, **dados.model_dump())
    except EmpresaNaoEncontradaError as erro:
        raise erro_http(status.HTTP_404_NOT_FOUND, str(erro)) from erro
    except InscricaoMunicipalJaExisteError as erro:
        raise erro_http(status.HTTP_409_CONFLICT, str(erro)) from erro
    except InscricaoMunicipalDadosInvalidosError as erro:
        raise erro_http(status.HTTP_422_UNPROCESSABLE_ENTITY, str(erro)) from erro


@router.get("", response_model=list[InscricaoMunicipalResponse])
def listar_inscricoes_municipais(
    empresa_id: int,
    sessao: Session = Depends(obter_sessao_api),
) -> list[InscricaoMunicipalResponse]:
    service = InscricaoMunicipalService(sessao)
    try:
        return service.listar_por_empresa(empresa_id)
    except EmpresaNaoEncontradaError as erro:
        raise erro_http(status.HTTP_404_NOT_FOUND, str(erro)) from erro
