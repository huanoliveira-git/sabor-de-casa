from fastapi import APIRouter

from app.api.dependencias import ServicoAutenticacao
from app.esquemas.autenticacao import LoginEntrada, TokenSaida

roteador = APIRouter(prefix="/auth", tags=["Autenticação"])


@roteador.post("/login", response_model=TokenSaida)
def entrar(dados: LoginEntrada, servico: ServicoAutenticacao) -> TokenSaida:
    token = servico.autenticar(dados.usuario, dados.senha)
    return TokenSaida(access_token=token)
