from fastapi import APIRouter

from app.api.rotas import autenticacao, categorias, pratos, saude

roteador_api = APIRouter(prefix="/api")
roteador_api.include_router(autenticacao.roteador)
roteador_api.include_router(categorias.roteador)
roteador_api.include_router(pratos.roteador)
roteador_api.include_router(saude.roteador)
