from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.rotas import roteador_api
from app.api.tratadores_erros import registrar_tratadores_de_erro
from app.config import Configuracoes, obter_configuracoes


def configurar_cors(aplicacao: FastAPI, configuracoes: Configuracoes) -> None:
    if configuracoes.lista_cors_origens:
        aplicacao.add_middleware(
            CORSMiddleware,
            allow_origins=configuracoes.lista_cors_origens,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def servir_front(aplicacao: FastAPI, pasta_front: Path) -> None:
    if pasta_front.is_dir():
        aplicacao.mount("/", StaticFiles(directory=pasta_front, html=True), name="front")


def criar_aplicacao() -> FastAPI:
    configuracoes = obter_configuracoes()
    aplicacao = FastAPI(
        title="Sabor de Casa - API",
        description="Serviço Web do cardápio digital da marmitaria Sabor de Casa.",
        version="1.0.0",
    )
    configurar_cors(aplicacao, configuracoes)
    registrar_tratadores_de_erro(aplicacao)
    aplicacao.include_router(roteador_api)
    servir_front(aplicacao, configuracoes.pasta_front)
    return aplicacao


app = criar_aplicacao()
