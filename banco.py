from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import obter_configuracoes


class Base(DeclarativeBase):
    pass


motor = create_engine(
    obter_configuracoes().url_banco_sqlalchemy,
    pool_pre_ping=True,
    pool_recycle=300,
)

FabricaDeSessao = sessionmaker(bind=motor, autoflush=False, expire_on_commit=False)


def obter_sessao() -> Iterator[Session]:
    with FabricaDeSessao() as sessao:
        yield sessao
