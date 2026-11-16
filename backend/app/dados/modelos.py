from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Numeric, String, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dados.banco import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(60))
    descricao: Mapped[str | None] = mapped_column(String(255))

    pratos: Mapped[list["Prato"]] = relationship(back_populates="categoria")


class Prato(Base):
    __tablename__ = "prato"

    id: Mapped[int] = mapped_column(primary_key=True)
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categoria.id", ondelete="RESTRICT"), index=True
    )
    nome: Mapped[str] = mapped_column(String(100))
    descricao: Mapped[str | None] = mapped_column(String(255))
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    disponivel: Mapped[bool] = mapped_column(Boolean, default=True, server_default=true())

    categoria: Mapped[Categoria] = relationship(back_populates="pratos")
