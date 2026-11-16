from app.dados.modelos import Prato
from app.dados.prato_repositorio import PratoRepositorio
from app.erros import RecursoNaoEncontrado
from app.esquemas.prato import PratoAtualizacao, PratoEntrada
from app.servicos.categoria_servico import CategoriaServico


class PratoServico:
    def __init__(self, repositorio: PratoRepositorio, categorias: CategoriaServico):
        self._repositorio = repositorio
        self._categorias = categorias

    def listar_por_categoria(self, categoria_id: int) -> list[Prato]:
        self._categorias.obter_existente(categoria_id)
        return self._repositorio.listar_por_categoria(categoria_id)

    def buscar(self, prato_id: int) -> Prato:
        prato = self._repositorio.buscar_por_id(prato_id)
        if prato is None:
            raise RecursoNaoEncontrado("Prato não encontrado.")
        return prato

    def criar(self, categoria_id: int, dados: PratoEntrada) -> Prato:
        self._categorias.obter_existente(categoria_id)
        prato = Prato(categoria_id=categoria_id, **dados.model_dump())
        return self._repositorio.salvar(prato)

    def atualizar(self, prato_id: int, dados: PratoAtualizacao) -> Prato:
        prato = self.buscar(prato_id)
        self._trocar_categoria_se_necessario(prato, dados.categoria_id)
        for campo, valor in dados.model_dump(exclude={"categoria_id"}).items():
            setattr(prato, campo, valor)
        return self._repositorio.salvar(prato)

    def excluir(self, prato_id: int) -> None:
        self._repositorio.excluir(self.buscar(prato_id))

    def _trocar_categoria_se_necessario(self, prato: Prato, nova_categoria_id: int | None) -> None:
        if nova_categoria_id is None or nova_categoria_id == prato.categoria_id:
            return
        self._categorias.obter_existente(nova_categoria_id)
        prato.categoria_id = nova_categoria_id
