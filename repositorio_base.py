from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.dados.banco import Base

Entidade = TypeVar("Entidade", bound=Base)


class RepositorioBase(Generic[Entidade]):
    modelo: type[Entidade]

    def __init__(self, sessao: Session):
        self._sessao = sessao

    def buscar_por_id(self, identificador: int) -> Entidade | None:
        return self._sessao.get(self.modelo, identificador)

    def salvar(self, entidade: Entidade) -> Entidade:
        self._sessao.add(entidade)
        self._sessao.commit()
        self._sessao.refresh(entidade)
        return entidade

    def excluir(self, entidade: Entidade) -> None:
        self._sessao.delete(entidade)
        self._sessao.commit()
