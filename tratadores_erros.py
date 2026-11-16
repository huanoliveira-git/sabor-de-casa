import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.erros import ErroAplicacao

logger = logging.getLogger(__name__)

MENSAGENS_DE_VALIDACAO = {
    "missing": "O campo {campo} é obrigatório.",
    "bool_parsing": "O campo {campo} deve ser verdadeiro ou falso.",
    "bool_type": "O campo {campo} deve ser verdadeiro ou falso.",
    "int_parsing": "O campo {campo} deve ser um número inteiro.",
    "int_type": "O campo {campo} deve ser um número inteiro.",
    "string_type": "O campo {campo} deve ser um texto.",
    "json_invalid": "Os dados enviados não estão em um formato JSON válido.",
    "model_attributes_type": "Os dados enviados devem ser um objeto JSON.",
}
NOMES_DOS_CAMPOS = {
    "descricao": "descrição",
    "preco": "preço",
    "disponivel": "disponível",
    "categoria_id": "categoria",
    "usuario": "usuário",
}
MENSAGENS_HTTP = {
    HTTPStatus.NOT_FOUND: "Recurso não encontrado.",
    HTTPStatus.METHOD_NOT_ALLOWED: "Operação não permitida.",
}


def resposta_de_erro(status: int, mensagem: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"detail": mensagem})


def traduzir_erro_de_validacao(erro: dict) -> str:
    if erro["type"] == "value_error":
        return str(erro["ctx"]["error"])
    campo = str(erro["loc"][-1]) if erro["loc"] else "informado"
    modelo = MENSAGENS_DE_VALIDACAO.get(erro["type"], "O campo {campo} é inválido.")
    return modelo.format(campo=NOMES_DOS_CAMPOS.get(campo, campo))


def mensagem_de_integridade(erro: IntegrityError) -> str:
    texto = str(erro.orig).lower()
    if "uq_categoria_nome_lower" in texto:
        return "Já existe uma categoria com esse nome."
    if "prato_categoria_id_fkey" in texto:
        return "Não é possível excluir uma categoria que ainda possui pratos."
    if "ck_prato_preco_positivo" in texto:
        return "O preço deve ser maior que zero."
    return "Os dados enviados violam uma regra do banco de dados."


async def tratar_erro_aplicacao(_: Request, erro: ErroAplicacao) -> JSONResponse:
    return resposta_de_erro(erro.status_http, erro.mensagem)


async def tratar_erro_validacao(_: Request, erro: RequestValidationError) -> JSONResponse:
    mensagens = dict.fromkeys(traduzir_erro_de_validacao(item) for item in erro.errors())
    return resposta_de_erro(HTTPStatus.UNPROCESSABLE_ENTITY, " ".join(mensagens))


async def tratar_erro_integridade(_: Request, erro: IntegrityError) -> JSONResponse:
    return resposta_de_erro(HTTPStatus.CONFLICT, mensagem_de_integridade(erro))


async def tratar_erro_conexao(_: Request, erro: OperationalError) -> JSONResponse:
    logger.error("Falha ao acessar o banco de dados: %s", erro)
    return resposta_de_erro(
        HTTPStatus.SERVICE_UNAVAILABLE,
        "Não foi possível acessar o banco de dados. Tente novamente em instantes.",
    )


async def tratar_erro_http(_: Request, erro: StarletteHTTPException) -> JSONResponse:
    mensagem = MENSAGENS_HTTP.get(erro.status_code, str(erro.detail))
    return resposta_de_erro(erro.status_code, mensagem)


async def tratar_erro_inesperado(_: Request, erro: Exception) -> JSONResponse:
    logger.exception("Erro inesperado: %s", erro)
    return resposta_de_erro(
        HTTPStatus.INTERNAL_SERVER_ERROR, "Ocorreu um erro inesperado no servidor."
    )


def registrar_tratadores_de_erro(aplicacao: FastAPI) -> None:
    aplicacao.add_exception_handler(ErroAplicacao, tratar_erro_aplicacao)
    aplicacao.add_exception_handler(RequestValidationError, tratar_erro_validacao)
    aplicacao.add_exception_handler(IntegrityError, tratar_erro_integridade)
    aplicacao.add_exception_handler(OperationalError, tratar_erro_conexao)
    aplicacao.add_exception_handler(StarletteHTTPException, tratar_erro_http)
    aplicacao.add_exception_handler(Exception, tratar_erro_inesperado)
