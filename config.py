from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PASTA_BACKEND = Path(__file__).resolve().parent.parent
PASTA_FRONT_PADRAO = PASTA_BACKEND.parent / "front"


class Configuracoes(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PASTA_BACKEND / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str
    admin_usuario: str
    admin_senha: str
    jwt_segredo: str
    jwt_algoritmo: str = "HS256"
    jwt_expiracao_minutos: int = 120
    pasta_front: Path = PASTA_FRONT_PADRAO
    cors_origens: str = ""

    @property
    def url_banco_sqlalchemy(self) -> str:
        url = self.database_url.strip()
        for prefixo in ("postgres://", "postgresql://"):
            if url.startswith(prefixo):
                return "postgresql+psycopg://" + url[len(prefixo):]
        return url

    @property
    def lista_cors_origens(self) -> list[str]:
        return [origem.strip() for origem in self.cors_origens.split(",") if origem.strip()]


@lru_cache
def obter_configuracoes() -> Configuracoes:
    return Configuracoes()
