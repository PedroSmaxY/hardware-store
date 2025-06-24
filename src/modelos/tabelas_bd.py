from typing import Optional
from sqlalchemy import Integer, String, Text, Numeric, Enum as SQLAlchemyEnum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.configs.config_bd import Base
import enum

"""
Este arquivo define os modelos de dados (ORM) para o sistema de vendas,
utilizando SQLAlchemy com Mapped Classes. Cada classe representa uma tabela
no banco de dados e suas respectivas colunas e relacionamentos, seguindo
o diagrama de entidades do sistema.
"""


class Produto(Base):
    __tablename__ = 'produto'

    id_produto: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(Text)
    quantidade_estoque: Mapped[int] = mapped_column(Integer, default=0)
    preco: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    itens_venda: Mapped[list["ItensVenda"]] = relationship(back_populates="produto")

    def __repr__(self):
        return f"<Produto(id_produto={self.id_produto}, nome='{self.nome}', preco={self.preco})>"


class Cliente(Base):
    __tablename__ = 'cliente'

    id_cliente: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    telefone: Mapped[Optional[str]] = mapped_column(String(15))

    vendas: Mapped[list["Venda"]] = relationship(back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(id_cliente={self.id_cliente}, nome='{self.nome}', cpf='{self.cpf}')>"


class CargoEnum(enum.Enum):
    GERENTE = 'Gerente'
    VENDEDOR = 'Vendedor'


class Funcionario(Base):
    __tablename__ = 'funcionario'

    id_funcionario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    cargo: Mapped[CargoEnum] = mapped_column(SQLAlchemyEnum(CargoEnum), nullable=False)
    nome_usuario: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)

    vendas: Mapped[list["Venda"]] = relationship(back_populates="funcionario")

    def __repr__(self):
        return f"<Funcionario(id_funcionario={self.id_funcionario}, nome='{self.nome}', cargo='{self.cargo.value}')>"


class Venda(Base):
    __tablename__ = 'venda'

    id_venda: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data_venda: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    id_funcionario: Mapped[int] = mapped_column(ForeignKey('funcionario.id_funcionario'), nullable=False)
    id_cliente: Mapped[Optional[int]] = mapped_column(ForeignKey('cliente.id_cliente'))

    valor_total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0.0)
    desconto_total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0.0)

    funcionario: Mapped["Funcionario"] = relationship(back_populates="vendas")
    cliente: Mapped[Optional["Cliente"]] = relationship(back_populates="vendas")
    itens_venda: Mapped[list["ItensVenda"]] = relationship(back_populates="venda")

    def __repr__(self):
        return f"<Venda(id_venda={self.id_venda}, data_venda='{self.data_venda}', valor_total={self.valor_total})>"


class ItensVenda(Base):
    __tablename__ = 'itens_venda'

    id_item_venda: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_venda: Mapped[int] = mapped_column(ForeignKey('venda.id_venda'), nullable=False)
    id_produto: Mapped[int] = mapped_column(ForeignKey('produto.id_produto'), nullable=False)

    quantidade: Mapped[int] = mapped_column(Integer, default=1)
    preco_unitario: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    desconto_aplicado: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), default=0.00)

    venda: Mapped["Venda"] = relationship(back_populates="itens_venda")
    produto: Mapped["Produto"] = relationship(back_populates="itens_venda")

    def __repr__(self):
        return (
            f"<ItensVenda(id_item_venda={self.id_item_venda}, id_venda={self.id_venda}, "
            f"id_produto={self.id_produto}, quantidade={self.quantidade})>"
        )
