from app.dados.categoria_repositorio import CategoriaRepositorio
from app.dados.modelos import Categoria
from app.erros import ConflitoDeDados, RecursoNaoEncontrado
from app.esquemas.categoria import CategoriaEntrada, CategoriaSaida


class CategoriaServico:
    def __init__(self, repositorio: CategoriaRepositorio):
        self._repositorio = repositorio

    def listar(self) -> list[CategoriaSaida]:
        return [
            _montar_saida(categoria, total)
            for categoria, total in self._repositorio.listar_com_total_de_pratos()
        ]

    def buscar(self, categoria_id: int) -> CategoriaSaida:
        categoria = self.obter_existente(categoria_id)
        return _montar_saida(categoria, self._repositorio.contar_pratos(categoria_id))

    def criar(self, dados: CategoriaEntrada) -> CategoriaSaida:
        self._garantir_nome_unico(dados.nome)
        categoria = self._repositorio.salvar(Categoria(**dados.model_dump()))
        return _montar_saida(categoria, total_pratos=0)

    def atualizar(self, categoria_id: int, dados: CategoriaEntrada) -> CategoriaSaida:
        categoria = self.obter_existente(categoria_id)
        self._garantir_nome_unico(dados.nome, ignorar_id=categoria_id)
        categoria.nome = dados.nome
        categoria.descricao = dados.descricao
        self._repositorio.salvar(categoria)
        return _montar_saida(categoria, self._repositorio.contar_pratos(categoria_id))

    def excluir(self, categoria_id: int) -> None:
        categoria = self.obter_existente(categoria_id)
        self._garantir_sem_pratos(categoria)
        self._repositorio.excluir(categoria)

    def obter_existente(self, categoria_id: int) -> Categoria:
        categoria = self._repositorio.buscar_por_id(categoria_id)
        if categoria is None:
            raise RecursoNaoEncontrado("Categoria não encontrada.")
        return categoria

    def _garantir_nome_unico(self, nome: str, ignorar_id: int | None = None) -> None:
        existente = self._repositorio.buscar_por_nome(nome)
        if existente is not None and existente.id != ignorar_id:
            raise ConflitoDeDados(f'Já existe uma categoria com o nome "{existente.nome}".')

    def _garantir_sem_pratos(self, categoria: Categoria) -> None:
        total = self._repositorio.contar_pratos(categoria.id)
        if total > 0:
            descricao_total = "1 prato" if total == 1 else f"{total} pratos"
            raise ConflitoDeDados(
                f'Não é possível excluir a categoria "{categoria.nome}" porque ela ainda '
                f"possui {descricao_total}. Exclua ou mova os pratos antes."
            )


def _montar_saida(categoria: Categoria, total_pratos: int) -> CategoriaSaida:
    return CategoriaSaida(
        id=categoria.id,
        nome=categoria.nome,
        descricao=categoria.descricao,
        total_pratos=total_pratos,
    )
