from typing import Optional
from sqlalchemy import Integer, String, Text, Numeric, Enum as SQLAlchemyEnum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.configs.config_bd import Base
import enum

"""
Este arquivo define os modelos de dados (ORM) para o sistema de vendas,
utilizando SQLAlchemy com Mapped Classes. Cada classe representa uma tabela
o banco de dados e suas respectivas colunas e relacionamentos, seguindo
o diagrama de entidades do sistema.
"""


class Produto(Base):
    """
    Representa um produto no banco de dados.

    Atributos:
        id_produto (int): O identificador único para o produto.
        nome (str): O nome do produto.
        descricao (Optional[str]): Uma descrição detalhada do produto.
        quantidade_estoque (int): A quantidade atual do produto em estoque.
        preco (float): O preço do produto.
        itens_venda (list[ItensVenda]): Uma lista de itens de venda associados a este produto.
    """
    __tablename__ = 'produto'

    id_produto: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    descricao: Mapped[Optional[str]] = mapped_column(Text)

    quantidade_estoque: Mapped[int] = mapped_column(Integer, default=0)

    preco: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    itens_venda: Mapped[list["ItensVenda"]] = relationship(
        back_populates="produto")

    def __repr__(self):
        return f"<Produto(id_produto={self.id_produto}, nome='{self.nome}', preco={self.preco})>"


class Cliente(Base):
    """
    Representa um cliente no banco de dados.

    Atributos:
        id_cliente (int): A chave primária para o cliente, autoincrementada.
        nome (str): O nome do cliente.
        cpf (str): O CPF do cliente, uma string única de 11 caracteres.
        telefone (Optional[str]): O número de telefone do cliente (pode ser nulo).
        vendas (list["Venda"]): Uma lista de objetos Venda, estabelece um relacionamento um-para-muitos com a tabela Venda.
    """

    __tablename__ = 'cliente'

    id_cliente: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)

    telefone: Mapped[Optional[str]] = mapped_column(String(15))

    vendas: Mapped[list["Venda"]] = relationship(back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(id_cliente={self.id_cliente}, nome='{self.nome}', cpf='{self.cpf}')>"


class CargoEnum(enum.Enum):
    """
    Representa os diferentes cargos possíveis para um funcionário.

    Atributos:
        GERENTE (str): Representa o cargo de Gerente, com valor 'Gerente'.
        VENDEDOR (str): Representa o cargo de Vendedor, com valor 'Vendedor'.
        ESTOQUISTA (str): Representa o cargo de Estoquista, com valor 'Estoquista'.
    """
    GERENTE = 'Gerente'
    VENDEDOR = 'Vendedor'
    ESTOQUISTA = 'Estoquista'


class Funcionario(Base):
    """
        Representa um funcionário no banco de dados.

        Atributos:
            id_funcionario (int): A chave primária para o funcionário, autoincrementada.
            nome (str): O nome completo do funcionário.
            cargo (CargoEnum): O cargo do funcionário, utilizando um enum para os valores permitidos.
            nome_usuario (str): O nome de usuário único para login do funcionário.
            senha (str): A senha do funcionário (geralmente armazenada como hash).
            vendas (list["Venda"]): Uma lista de objetos Venda, estabelece um relacionamento um-para-muitos com a tabela Venda, indicando as vendas realizadas por este funcionário.
    """
    __tablename__ = 'funcionario'

    id_funcionario: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    cargo: Mapped[CargoEnum] = mapped_column(
        SQLAlchemyEnum(CargoEnum), nullable=False)

    nome_usuario: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)

    senha: Mapped[str] = mapped_column(String(255), nullable=False)

    vendas: Mapped[list["Venda"]] = relationship(back_populates="funcionario")

    def __repr__(self):
        return f"<Funcionario(id_funcionario={self.id_funcionario}, nome='{self.nome}', cargo='{self.cargo.value}')>"


class Venda(Base):
    """
        Representa uma venda no banco de dados.
        
        Atributos:
            id_venda (int): A chave primária para a venda, autoincrementada.
            data_venda (DateTime): A data e hora em que a venda foi realizada. Não pode ser nula.
            id_funcionario (int): A chave estrangeira referenciando o funcionário que realizou a venda. Não pode ser nula.
            id_cliente (Optional[int]): A chave estrangeira referenciando o cliente associado à venda (pode ser nula).
            valor_total (float): O valor total da venda, armazenado como um número com 10 dígitos no total e 2 casas decimais. Não pode ser nulo.
            funcionario (Funcionario): O objeto Funcionario associado a esta venda. Estabelece um relacionamento com a tabela Funcionario.
            cliente (Optional[Cliente]): O objeto Cliente opcionalmente associado a esta venda. Estabelece um relacionamento com a tabela Cliente.
            itens_venda (list["ItensVenda"]): Uma lista de objetos ItensVenda associados a esta venda. Estabelece um relacionamento um-para-muitos com a tabela ItensVenda.
    """

    __tablename__ = 'venda'

    id_venda: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    data_venda: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    id_funcionario: Mapped[int] = mapped_column(
        ForeignKey('funcionario.id_funcionario'), nullable=False)

    id_cliente: Mapped[Optional[int]] = mapped_column(
        ForeignKey('cliente.id_cliente'))

    valor_total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    funcionario: Mapped["Funcionario"] = relationship(back_populates="vendas")

    cliente: Mapped[Optional["Cliente"]] = relationship(
        back_populates="vendas")

    itens_venda: Mapped[list["ItensVenda"]
                        ] = relationship(back_populates="venda")

    def __repr__(self):
        return f"<Venda(id_venda={self.id_venda}, data_venda='{self.data_venda}', valor_total={self.valor_total})>"


class ItensVenda(Base):
    """
        Representa um item de uma venda no banco de dados.

        Esta classe mapeia a tabela 'itens_venda' e armazena os detalhes
        de cada produto incluído em uma venda específica, como a quantidade,
        o preço unitário no momento da venda e qualquer desconto aplicado.
        
        Atributos:
            id_item_venda (int): A chave primária para o item da venda, autoincrementada.
            id_venda (int): A chave estrangeira que referencia o ID da venda na tabela 'venda'. Não pode ser nula.
            id_produto (int): A chave estrangeira que referencia o ID do produto na tabela 'produto'. Não pode ser nula.
            quantidade (int): A quantidade do produto vendido neste item. O valor padrão é 1.
            preco_unitario (float): O preço unitário do produto no momento da venda. Armazenado como Numeric(10, 2). Não pode ser nulo.
            desconto_aplicado (Optional[float]): O valor do desconto aplicado a este item da venda. Armazenado como Numeric(5, 2). O valor padrão é 0.00.
            venda (Venda): O objeto Venda ao qual este item pertence. Estabelece um relacionamento muitos-para-um com a tabela 'venda'.
            produto (Produto): O objeto Produto que foi vendido neste item. Estabelece um relacionamento muitos-para-um com a tabela 'produto'.
    """

    __tablename__ = 'itens_venda'

    id_item_venda: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    id_venda: Mapped[int] = mapped_column(
        ForeignKey('venda.id_venda'), nullable=False)

    id_produto: Mapped[int] = mapped_column(
        ForeignKey('produto.id_produto'), nullable=False)

    quantidade: Mapped[int] = mapped_column(Integer, default=1)

    preco_unitario: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=False)

    desconto_aplicado: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2), default=0.00)

    venda: Mapped["Venda"] = relationship(back_populates="itens_venda")

    produto: Mapped["Produto"] = relationship(back_populates="itens_venda")

    def __repr__(self):
        return f"<ItensVenda(id_item_venda={self.id_item_venda}, id_venda={self.id_venda}, id_produto={self.id_produto}, quantidade={self.quantidade})>"
