from http import HTTPStatus

from fastapi import APIRouter

from app.api.dependencias import ApenasAdministrador, ServicoPrato
from app.dados.modelos import Prato
from app.esquemas.prato import PratoAtualizacao, PratoEntrada, PratoSaida

roteador = APIRouter(tags=["Pratos"])


@roteador.get("/categorias/{categoria_id}/pratos", response_model=list[PratoSaida])
def listar_pratos_da_categoria(categoria_id: int, servico: ServicoPrato) -> list[Prato]:
    return servico.listar_por_categoria(categoria_id)


@roteador.post(
    "/categorias/{categoria_id}/pratos",
    response_model=PratoSaida,
    status_code=HTTPStatus.CREATED,
    dependencies=ApenasAdministrador,
)
def criar_prato(categoria_id: int, dados: PratoEntrada, servico: ServicoPrato) -> Prato:
    return servico.criar(categoria_id, dados)


@roteador.get("/pratos/{prato_id}", response_model=PratoSaida)
def buscar_prato(prato_id: int, servico: ServicoPrato) -> Prato:
    return servico.buscar(prato_id)


@roteador.put("/pratos/{prato_id}", response_model=PratoSaida, dependencies=ApenasAdministrador)
def atualizar_prato(prato_id: int, dados: PratoAtualizacao, servico: ServicoPrato) -> Prato:
    return servico.atualizar(prato_id, dados)


@roteador.delete(
    "/pratos/{prato_id}", status_code=HTTPStatus.NO_CONTENT, dependencies=ApenasAdministrador
)
def excluir_prato(prato_id: int, servico: ServicoPrato) -> None:
    servico.excluir(prato_id)
