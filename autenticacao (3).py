from pydantic import BaseModel, field_validator

from app.esquemas.validadores import validar_texto_obrigatorio


class LoginEntrada(BaseModel):
    usuario: str
    senha: str

    @field_validator("usuario", mode="before")
    @classmethod
    def validar_usuario(cls, valor: object) -> str:
        return validar_texto_obrigatorio(valor, "usuário", limite=100)

    @field_validator("senha", mode="before")
    @classmethod
    def validar_senha(cls, valor: object) -> str:
        if not isinstance(valor, str) or not valor:
            raise ValueError("O campo senha é obrigatório.")
        return valor


class TokenSaida(BaseModel):
    access_token: str
    token_type: str = "bearer"
