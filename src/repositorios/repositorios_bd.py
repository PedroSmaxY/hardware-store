
from typing import List, Optional
from sqlalchemy.orm import Session
from src.configs.config_bd import Session as SessionLocal
from src.modelos.tabelas_bd import Produto, Cliente, Funcionario, Venda, ItensVenda

"""
Este arquivo implementa as classes de repositório para acesso aos dados do sistema
de loja de hardware, seguindo o padrão Repository. Cada repositório encapsula
as operações CRUD específicas de uma entidade, fornecendo uma camada de abstração
entre os modelos de dados e a lógica de negócio da aplicação.
"""

# TODO: Implementar as classes de repositório com as operações CRUD necessárias


class ProdutoRepositorio:
    """Repositório para operações CRUD da entidade Produto."""

    def __init__(self, session: Session = None):
        self.session = session or SessionLocal()

    def criar(self, produto: Produto) -> Produto:
        pass

    def buscar_por_id(self, id_produto: int) -> Optional[Produto]:
        pass

    def buscar_todos(self) -> List[Produto]:
        pass

    def buscar_por_nome(self, nome: str) -> List[Produto]:
        pass

    def atualizar(self, produto: Produto) -> Produto:
        pass

    def deletar(self, id_produto: int) -> bool:
        pass

    def atualizar_estoque(self, id_produto: int, nova_quantidade: int) -> bool:
        pass


class ClienteRepositorio:
    """Repositório para operações CRUD da entidade Cliente."""

    def __init__(self, session: Session = None):
        self.session = session or SessionLocal()

    def criar(self, cliente: Cliente) -> Cliente:
        pass

    def buscar_por_id(self, id_cliente: int) -> Optional[Cliente]:
        pass

    def buscar_todos(self) -> List[Cliente]:
        pass

    def buscar_por_cpf(self, cpf: str) -> Optional[Cliente]:
        pass

    def buscar_por_nome(self, nome: str) -> List[Cliente]:
        pass

    def atualizar(self, cliente: Cliente) -> Cliente:
        pass

    def deletar(self, id_cliente: int) -> bool:
        pass


class FuncionarioRepositorio:
    """Repositório para operações CRUD da entidade Funcionario."""

    def __init__(self, session: Session = None):
        self.session = session or SessionLocal()

    def criar(self, funcionario: Funcionario) -> Funcionario:
        pass

    def buscar_por_id(self, id_funcionario: int) -> Optional[Funcionario]:
        pass

    def buscar_todos(self) -> List[Funcionario]:
        pass

    def buscar_por_nome_usuario(self, nome_usuario: str) -> Optional[Funcionario]:
        pass

    def buscar_por_cargo(self, cargo: str) -> List[Funcionario]:
        pass

    def atualizar(self, funcionario: Funcionario) -> Funcionario:
        pass

    def deletar(self, id_funcionario: int) -> bool:
        pass

    def autenticar(self, nome_usuario: str, senha: str) -> Optional[Funcionario]:
        pass


class VendaRepositorio:
    """Repositório para operações CRUD da entidade Venda."""

    def __init__(self, session: Session = None):
        self.session = session or SessionLocal()

    def criar(self, venda: Venda) -> Venda:
        pass

    def buscar_por_id(self, id_venda: int) -> Optional[Venda]:
        pass

    def buscar_todas(self) -> List[Venda]:
        pass

    def buscar_por_funcionario(self, id_funcionario: int) -> List[Venda]:
        pass

    def buscar_por_cliente(self, id_cliente: int) -> List[Venda]:
        pass

    def buscar_por_periodo(self, data_inicio, data_fim) -> List[Venda]:
        pass

    def atualizar(self, venda: Venda) -> Venda:
        pass

    def deletar(self, id_venda: int) -> bool:
        pass


class ItensVendaRepositorio:
    """Repositório para operações CRUD da entidade ItensVenda."""

    def __init__(self, session: Session = None):
        self.session = session or SessionLocal()

    def criar(self, item_venda: ItensVenda) -> ItensVenda:
        pass

    def buscar_por_id(self, id_item_venda: int) -> Optional[ItensVenda]:
        pass

    def buscar_por_venda(self, id_venda: int) -> List[ItensVenda]:
        pass

    def buscar_por_produto(self, id_produto: int) -> List[ItensVenda]:
        pass

    def atualizar(self, item_venda: ItensVenda) -> ItensVenda:
        pass

    def deletar(self, id_item_venda: int) -> bool:
        pass

    def calcular_subtotal(self, id_item_venda: int) -> float:
        pass
