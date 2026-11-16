import sys
from pathlib import Path

PASTA_BACKEND = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA_BACKEND))

from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import Configuracoes
from app.dados.banco import Base
from app.dados.categoria_repositorio import CategoriaRepositorio
from app.dados.prato_repositorio import PratoRepositorio
from app.erros import ConflitoDeDados, NaoAutenticado, RecursoNaoEncontrado
from app.esquemas.categoria import CategoriaEntrada
from app.esquemas.prato import PratoAtualizacao, PratoEntrada
from app.servicos.autenticacao_servico import AutenticacaoServico
from app.servicos.categoria_servico import CategoriaServico
from app.servicos.prato_servico import PratoServico


def criar_servicos():
    motor = create_engine("sqlite://")
    Base.metadata.create_all(motor)
    sessao = sessionmaker(bind=motor, autoflush=False, expire_on_commit=False)()
    cat_srv = CategoriaServico(CategoriaRepositorio(sessao))
    prato_srv = PratoServico(PratoRepositorio(sessao), cat_srv)
    auth_srv = AutenticacaoServico(
        Configuracoes(
            database_url="sqlite://",
            admin_usuario="admin",
            admin_senha="123",
            jwt_segredo="segredo-de-teste-com-mais-de-32-bytes-123456",
        )
    )
    return cat_srv, prato_srv, auth_srv


def main() -> None:
    cat_srv, prato_srv, auth_srv = criar_servicos()

    token = auth_srv.autenticar("admin", "123")
    assert auth_srv.validar_token(token) == "admin"
    print("[OK] 1. Login e geração/validação de token JWT")

    try:
        auth_srv.autenticar("admin", "errada")
        raise AssertionError("Deveria falhar")
    except NaoAutenticado as e:
        assert e.status_http == 401
    print("[OK] 2. Rejeição de senha incorreta (401)")

    c1 = cat_srv.criar(CategoriaEntrada(nome="Marmitas", descricao="Pratos do dia"))
    assert c1.total_pratos == 0
    print("[OK] 3. Criação de categoria")

    try:
        cat_srv.criar(CategoriaEntrada(nome="  marmitas "))
        raise AssertionError("Deveria bloquear nome repetido")
    except ConflitoDeDados as e:
        assert e.status_http == 409
    print("[OK] 4. Regra Cenário 3: bloqueio de nome de categoria repetido (409)")

    try:
        PratoEntrada(nome="Teste", preco="0")
        raise AssertionError("Deveria bloquear preço <= 0")
    except ValidationError:
        pass
    print("[OK] 5. Regra Cenário 3: bloqueio de preço menor ou igual a zero (422)")

    try:
        CategoriaEntrada(nome="   ")
        raise AssertionError("Deveria bloquear nome vazio")
    except ValidationError:
        pass
    print("[OK] 6. Regra Cenário 3: bloqueio de campos obrigatórios vazios (422)")

    p1 = prato_srv.criar(c1.id, PratoEntrada(nome="Frango Grelhado", preco="18,90"))
    assert str(p1.preco) == "18.90"
    print("[OK] 7. Criação de prato com conversão de preço com vírgula (18,90 -> 18.90)")

    try:
        cat_srv.excluir(c1.id)
        raise AssertionError("Deveria impedir exclusão de categoria com pratos")
    except ConflitoDeDados as e:
        assert e.status_http == 409
    print("[OK] 8. Regra Cenário 3: bloqueio de exclusão de categoria com pratos (409)")

    p1_edit = prato_srv.atualizar(
        p1.id,
        PratoAtualizacao(
            nome="Frango Especial",
            descricao="Completo",
            preco="22.50",
            disponivel=False,
            categoria_id=c1.id,
        ),
    )
    assert str(p1_edit.preco) == "22.50" and p1_edit.disponivel is False
    print("[OK] 9. Atualização de prato")

    prato_srv.excluir(p1.id)
    cat_srv.excluir(c1.id)
    try:
        cat_srv.buscar(c1.id)
        raise AssertionError("Deveria retornar 404")
    except RecursoNaoEncontrado as e:
        assert e.status_http == 404
    print("[OK] 10. Exclusão de prato e posterior exclusão da categoria vazia")

    print("\nTodos os 10 testes de regras de negócio e CRUD passaram com sucesso!")


if __name__ == "__main__":
    main()
