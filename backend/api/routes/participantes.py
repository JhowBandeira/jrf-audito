"""Rotas HTTP de participantes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.dependencies import obter_sessao_api
from backend.schemas.participante import ParticipanteCreate, ParticipanteResponse
from backend.services.empresa_service import EmpresaNaoEncontradaError
from backend.services.participante_service import (
    ParticipanteDadosInvalidosError,
    ParticipanteJaExisteError,
    ParticipanteNaoEncontradoError,
    ParticipanteService,
)

router = APIRouter(prefix="/empresas/{empresa_id}/participantes", tags=["participantes"])


def erro_http(status_code: int, mensagem: str) -> HTTPException:
    """Cria erro HTTP simples e consistente para a API."""
    return HTTPException(status_code=status_code, detail=mensagem)


@router.post("", response_model=ParticipanteResponse, status_code=status.HTTP_201_CREATED)
def criar_participante(empresa_id: int, dados: ParticipanteCreate, sessao: Session = Depends(obter_sessao_api)) -> ParticipanteResponse:
    service = ParticipanteService(sessao)
    try:
        return service.criar_participante(empresa_id=empresa_id, **dados.model_dump())
    except EmpresaNaoEncontradaError as erro:
        raise erro_http(status.HTTP_404_NOT_FOUND, str(erro)) from erro
    except ParticipanteJaExisteError as erro:
        raise erro_http(status.HTTP_409_CONFLICT, str(erro)) from erro
    except ParticipanteDadosInvalidosError as erro:
        raise erro_http(status.HTTP_422_UNPROCESSABLE_ENTITY, str(erro)) from erro


@router.get("", response_model=list[ParticipanteResponse])
def listar_participantes(empresa_id: int, sessao: Session = Depends(obter_sessao_api)) -> list[ParticipanteResponse]:
    service = ParticipanteService(sessao)
    try:
        return service.listar_por_empresa(empresa_id)
    except EmpresaNaoEncontradaError as erro:
        raise erro_http(status.HTTP_404_NOT_FOUND, str(erro)) from erro


@router.get("/documento/{cpf_cnpj:path}", response_model=ParticipanteResponse)
def buscar_participante_por_documento(empresa_id: int, cpf_cnpj: str, sessao: Session = Depends(obter_sessao_api)) -> ParticipanteResponse:
    service = ParticipanteService(sessao)
    try:
        return service.obter_por_cpf_cnpj(empresa_id, cpf_cnpj)
    except EmpresaNaoEncontradaError as erro:
        raise erro_http(status.HTTP_404_NOT_FOUND, str(erro)) from erro
    except ParticipanteNaoEncontradoError as erro:
        raise erro_http(status.HTTP_404_NOT_FOUND, str(erro)) from erro
    except ParticipanteDadosInvalidosError as erro:
        raise erro_http(status.HTTP_422_UNPROCESSABLE_ENTITY, str(erro)) from erro


@router.get("/{participante_id}", response_model=ParticipanteResponse)
def buscar_participante_por_id(empresa_id: int, participante_id: int, sessao: Session = Depends(obter_sessao_api)) -> ParticipanteResponse:
    service = ParticipanteService(sessao)
    try:
        return service.obter_por_id(empresa_id, participante_id)
    except EmpresaNaoEncontradaError as erro:
        raise erro_http(status.HTTP_404_NOT_FOUND, str(erro)) from erro
    except ParticipanteNaoEncontradoError as erro:
        raise erro_http(status.HTTP_404_NOT_FOUND, str(erro)) from erro
