from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config import obter_configuracoes
from app.dados.banco import obter_sessao
from app.dados.categoria_repositorio import CategoriaRepositorio
from app.dados.prato_repositorio import PratoRepositorio
from app.erros import NaoAutenticado
from app.servicos.autenticacao_servico import AutenticacaoServico
from app.servicos.categoria_servico import CategoriaServico
from app.servicos.prato_servico import PratoServico

SessaoBanco = Annotated[Session, Depends(obter_sessao)]
esquema_bearer = HTTPBearer(auto_error=False)


def obter_autenticacao_servico() -> AutenticacaoServico:
    return AutenticacaoServico(obter_configuracoes())


def obter_categoria_servico(sessao: SessaoBanco) -> CategoriaServico:
    return CategoriaServico(CategoriaRepositorio(sessao))


def obter_prato_servico(sessao: SessaoBanco) -> PratoServico:
    categorias = CategoriaServico(CategoriaRepositorio(sessao))
    return PratoServico(PratoRepositorio(sessao), categorias)


ServicoAutenticacao = Annotated[AutenticacaoServico, Depends(obter_autenticacao_servico)]
ServicoCategoria = Annotated[CategoriaServico, Depends(obter_categoria_servico)]
ServicoPrato = Annotated[PratoServico, Depends(obter_prato_servico)]


def exigir_administrador(
    servico: ServicoAutenticacao,
    credenciais: Annotated[HTTPAuthorizationCredentials | None, Depends(esquema_bearer)],
) -> str:
    if credenciais is None:
        raise NaoAutenticado("Entre na área de gerenciamento para continuar.")
    return servico.validar_token(credenciais.credentials)


ApenasAdministrador = [Depends(exigir_administrador)]
