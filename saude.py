from fastapi import APIRouter
from sqlalchemy import text

from app.api.dependencias import SessaoBanco

roteador = APIRouter(tags=["Saúde"])


@roteador.get("/saude")
def verificar_saude(sessao: SessaoBanco) -> dict[str, str]:
    sessao.execute(text("SELECT 1"))
    return {"api": "ok", "banco": "ok"}
