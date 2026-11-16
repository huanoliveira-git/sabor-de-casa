import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("ADMIN_USUARIO", "admin")
os.environ.setdefault("ADMIN_SENHA", "senha-teste")
os.environ.setdefault("JWT_SEGREDO", "segredo-de-teste-com-tamanho-suficiente-32")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.dados.banco import Base, obter_sessao
from app.main import app


@pytest.fixture()
def cliente():
    motor = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(motor)
    fabrica = sessionmaker(bind=motor, autoflush=False, expire_on_commit=False)

    def sessao_de_teste():
        with fabrica() as sessao:
            yield sessao

    app.dependency_overrides[obter_sessao] = sessao_de_teste
    with TestClient(app) as cliente_http:
        yield cliente_http
    app.dependency_overrides.clear()


@pytest.fixture()
def admin(cliente):
    resposta = cliente.post("/api/auth/login", json={"usuario": "admin", "senha": "senha-teste"})
    cliente.headers["Authorization"] = f"Bearer {resposta.json()['access_token']}"
    return cliente
