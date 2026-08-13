"""Rotas HTTP de empresas."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.dependencies import obter_sessao_api
from backend.schemas.empresa import EmpresaCreate, EmpresaResponse
from backend.services.empresa_service import (
    EmpresaDadosInvalidosError,
    EmpresaJaExisteError,
    EmpresaNaoEncontradaError,
    EmpresaService,
)

router = APIRouter(prefix="/empresas", tags=["empresas"])


def erro_http(status_code: int, mensagem: str) -> HTTPException:
    """Cria erro HTTP simples e consistente para a API."""
    return HTTPException(status_code=status_code, detail=mensagem)


@router.post("", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
def criar_empresa(
    dados: EmpresaCreate,
    sessao: Session = Depends(obter_sessao_api),
) -> EmpresaResponse:
    service = EmpresaService(sessao)
    try:
        return service.criar_empresa(**dados.model_dump())
    except EmpresaJaExisteError as erro:
        raise erro_http(status.HTTP_409_CONFLICT, str(erro)) from erro
    except EmpresaDadosInvalidosError as erro:
        raise erro_http(status.HTTP_422_UNPROCESSABLE_ENTITY, str(erro)) from erro


@router.get("", response_model=list[EmpresaResponse])
def listar_empresas(sessao: Session = Depends(obter_sessao_api)) -> list[EmpresaResponse]:
    service = EmpresaService(sessao)
    return service.listar_empresas()


@router.get("/cnpj/{cnpj}", response_model=EmpresaResponse)
def buscar_empresa_por_cnpj(
    cnpj: str,
    sessao: Session = Depends(obter_sessao_api),
) -> EmpresaResponse:
    service = EmpresaService(sessao)
    try:
        return service.obter_empresa_por_cnpj(cnpj)
    except EmpresaNaoEncontradaError as erro:
        raise erro_http(status.HTTP_404_NOT_FOUND, str(erro)) from erro
    except EmpresaDadosInvalidosError as erro:
        raise erro_http(status.HTTP_422_UNPROCESSABLE_ENTITY, str(erro)) from erro


@router.get("/{empresa_id}", response_model=EmpresaResponse)
def buscar_empresa_por_id(
    empresa_id: int,
    sessao: Session = Depends(obter_sessao_api),
) -> EmpresaResponse:
    service = EmpresaService(sessao)
    try:
        return service.obter_empresa_por_id(empresa_id)
    except EmpresaNaoEncontradaError as erro:
        raise erro_http(status.HTTP_404_NOT_FOUND, str(erro)) from erro
