from sqlalchemy import select

from app.dados.modelos import Prato
from app.dados.repositorio_base import RepositorioBase


class PratoRepositorio(RepositorioBase[Prato]):
    modelo = Prato

    def listar_por_categoria(self, categoria_id: int) -> list[Prato]:
        consulta = (
            select(Prato)
            .where(Prato.categoria_id == categoria_id)
            .order_by(Prato.nome)
        )
        return list(self._sessao.scalars(consulta))
