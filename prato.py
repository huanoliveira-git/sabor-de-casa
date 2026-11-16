from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator

from app.esquemas.validadores import (
    validar_preco,
    validar_texto_obrigatorio,
    validar_texto_opcional,
)


class PratoEntrada(BaseModel):
    nome: str
    descricao: str | None = None
    preco: Decimal
    disponivel: bool = True

    @field_validator("nome", mode="before")
    @classmethod
    def validar_nome(cls, valor: object) -> str:
        return validar_texto_obrigatorio(valor, "nome", limite=100)

    @field_validator("descricao", mode="before")
    @classmethod
    def validar_descricao(cls, valor: object) -> str | None:
        return validar_texto_opcional(valor, "descrição", limite=255)

    @field_validator("preco", mode="before")
    @classmethod
    def converter_preco(cls, valor: object) -> Decimal:
        return validar_preco(valor)


class PratoAtualizacao(PratoEntrada):
    categoria_id: int | None = None


class PratoSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    categoria_id: int
    nome: str
    descricao: str | None
    preco: Decimal
    disponivel: bool
