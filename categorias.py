from http import HTTPStatus

from fastapi import APIRouter

from app.api.dependencias import ApenasAdministrador, ServicoCategoria
from app.esquemas.categoria import CategoriaEntrada, CategoriaSaida

roteador = APIRouter(prefix="/categorias", tags=["Categorias"])


@roteador.get("", response_model=list[CategoriaSaida])
def listar_categorias(servico: ServicoCategoria) -> list[CategoriaSaida]:
    return servico.listar()


@roteador.get("/{categoria_id}", response_model=CategoriaSaida)
def buscar_categoria(categoria_id: int, servico: ServicoCategoria) -> CategoriaSaida:
    return servico.buscar(categoria_id)


@roteador.post(
    "",
    response_model=CategoriaSaida,
    status_code=HTTPStatus.CREATED,
    dependencies=ApenasAdministrador,
)
def criar_categoria(dados: CategoriaEntrada, servico: ServicoCategoria) -> CategoriaSaida:
    return servico.criar(dados)


@roteador.put("/{categoria_id}", response_model=CategoriaSaida, dependencies=ApenasAdministrador)
def atualizar_categoria(
    categoria_id: int, dados: CategoriaEntrada, servico: ServicoCategoria
) -> CategoriaSaida:
    return servico.atualizar(categoria_id, dados)


@roteador.delete(
    "/{categoria_id}", status_code=HTTPStatus.NO_CONTENT, dependencies=ApenasAdministrador
)
def excluir_categoria(categoria_id: int, servico: ServicoCategoria) -> None:
    servico.excluir(categoria_id)
