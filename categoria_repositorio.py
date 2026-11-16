from sqlalchemy import func, select

from app.dados.modelos import Categoria, Prato
from app.dados.repositorio_base import RepositorioBase


class CategoriaRepositorio(RepositorioBase[Categoria]):
    modelo = Categoria

    def listar_com_total_de_pratos(self) -> list[tuple[Categoria, int]]:
        consulta = (
            select(Categoria, func.count(Prato.id))
            .outerjoin(Prato, Prato.categoria_id == Categoria.id)
            .group_by(Categoria.id)
            .order_by(Categoria.nome)
        )
        return [(categoria, total) for categoria, total in self._sessao.execute(consulta)]

    def buscar_por_nome(self, nome: str) -> Categoria | None:
        consulta = select(Categoria).where(func.lower(Categoria.nome) == nome.lower())
        return self._sessao.scalars(consulta).first()

    def contar_pratos(self, categoria_id: int) -> int:
        consulta = select(func.count(Prato.id)).where(Prato.categoria_id == categoria_id)
        return self._sessao.scalar(consulta) or 0
