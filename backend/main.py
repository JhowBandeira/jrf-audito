"""Ponto de entrada da API JRF-Audito."""

from fastapi import FastAPI

from backend.api.routes.empresas import router as empresas_router
from backend.api.routes.inscricoes_estaduais import router as inscricoes_estaduais_router
from backend.api.routes.inscricoes_municipais import router as inscricoes_municipais_router
from backend.api.routes.participantes import router as participantes_router

app = FastAPI(title="JRF-Audito", version="0.1.0")


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(empresas_router)
app.include_router(inscricoes_estaduais_router)
app.include_router(inscricoes_municipais_router)
app.include_router(participantes_router)
