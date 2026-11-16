from pydantic import BaseModel, ConfigDict, field_validator

from app.esquemas.validadores import validar_texto_obrigatorio, validar_texto_opcional


class CategoriaEntrada(BaseModel):
    nome: str
    descricao: str | None = None

    @field_validator("nome", mode="before")
    @classmethod
    def validar_nome(cls, valor: object) -> str:
        return validar_texto_obrigatorio(valor, "nome", limite=60)

    @field_validator("descricao", mode="before")
    @classmethod
    def validar_descricao(cls, valor: object) -> str | None:
        return validar_texto_opcional(valor, "descrição", limite=255)


class CategoriaSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descricao: str | None
    total_pratos: int = 0
