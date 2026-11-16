import secrets
from datetime import datetime, timedelta, timezone

import jwt

from app.config import Configuracoes
from app.erros import NaoAutenticado


class AutenticacaoServico:
    def __init__(self, configuracoes: Configuracoes):
        self._config = configuracoes

    def autenticar(self, usuario: str, senha: str) -> str:
        if not self._credenciais_conferem(usuario, senha):
            raise NaoAutenticado("Usuário ou senha inválidos.")
        return self._gerar_token(usuario)

    def validar_token(self, token: str) -> str:
        try:
            dados = jwt.decode(
                token, self._config.jwt_segredo, algorithms=[self._config.jwt_algoritmo]
            )
        except jwt.ExpiredSignatureError:
            raise NaoAutenticado("Sua sessão expirou. Entre novamente.") from None
        except jwt.InvalidTokenError:
            raise NaoAutenticado("Acesso não autorizado. Entre novamente.") from None
        return dados["sub"]

    def _credenciais_conferem(self, usuario: str, senha: str) -> bool:
        usuario_ok = secrets.compare_digest(usuario.encode(), self._config.admin_usuario.encode())
        senha_ok = secrets.compare_digest(senha.encode(), self._config.admin_senha.encode())
        return usuario_ok and senha_ok

    def _gerar_token(self, usuario: str) -> str:
        expiracao = datetime.now(timezone.utc) + timedelta(
            minutes=self._config.jwt_expiracao_minutos
        )
        return jwt.encode(
            {"sub": usuario, "exp": expiracao},
            self._config.jwt_segredo,
            algorithm=self._config.jwt_algoritmo,
        )
