
from typing import List, Optional
from datetime import datetime
from src.repositorios import (
    ProdutoRepositorio, ClienteRepositorio, FuncionarioRepositorio,
    VendaRepositorio, ItensVendaRepositorio
)
from src.modelos.tabelas_bd import Produto, Cliente, Funcionario, Venda, ItensVenda, CargoEnum

"""
Este arquivo implementa as classes de serviço para a lógica de negócio do sistema
de loja de hardware, seguindo o padrão Service Layer. Cada serviço encapsula
as regras de negócio específicas de uma entidade, coordenando operações entre
repositórios e aplicando validações necessárias antes das operações de dados.
"""

# TODO: Implementar as classes de serviço com as regras de negócio necessárias


class ProdutoServico:
    """Serviço para regras de negócio da entidade Produto."""

    def __init__(self):
        self.produto_repo = ProdutoRepositorio()

    def criar_produto(self, nome: str, descricao: str, quantidade_estoque: int, preco: float) -> Produto:
        pass

    def buscar_produto_por_id(self, id_produto: int) -> Optional[Produto]:
        pass

    def buscar_todos_produtos(self) -> List[Produto]:
        pass

    def buscar_produtos_por_nome(self, nome: str) -> List[Produto]:
        pass

    def atualizar_produto(self, id_produto: int, nome: str = None, descricao: str = None,
                          quantidade_estoque: int = None, preco: float = None) -> Produto:
        pass

    def deletar_produto(self, id_produto: int) -> bool:
        pass

    def verificar_estoque_disponivel(self, id_produto: int, quantidade_solicitada: int) -> bool:
        pass

    def atualizar_estoque(self, id_produto: int, nova_quantidade: int) -> bool:
        pass

    def reduzir_estoque(self, id_produto: int, quantidade: int) -> bool:
        pass


class ClienteServico:
    """Serviço para regras de negócio da entidade Cliente."""

    def __init__(self):
        self.cliente_repo = ClienteRepositorio()

    def criar_cliente(self, nome: str, cpf: str, telefone: str = None) -> Cliente:
        pass

    def buscar_cliente_por_id(self, id_cliente: int) -> Optional[Cliente]:
        pass

    def buscar_todos_clientes(self) -> List[Cliente]:
        pass

    def buscar_cliente_por_cpf(self, cpf: str) -> Optional[Cliente]:
        pass

    def buscar_clientes_por_nome(self, nome: str) -> List[Cliente]:
        pass

    def atualizar_cliente(self, id_cliente: int, nome: str = None,
                          telefone: str = None) -> Cliente:
        pass

    def deletar_cliente(self, id_cliente: int) -> bool:
        pass

    def validar_cpf(self, cpf: str) -> bool:
        pass

    def verificar_cpf_existente(self, cpf: str) -> bool:
        pass


class FuncionarioServico:
    """Serviço para regras de negócio da entidade Funcionario."""

    def __init__(self):
        self.funcionario_repo = FuncionarioRepositorio()

    def criar_funcionario(self, nome: str, cargo: CargoEnum, nome_usuario: str, senha: str) -> Funcionario:
        pass

    def buscar_funcionario_por_id(self, id_funcionario: int) -> Optional[Funcionario]:
        pass

    def buscar_todos_funcionarios(self) -> List[Funcionario]:
        pass

    def buscar_funcionario_por_nome_usuario(self, nome_usuario: str) -> Optional[Funcionario]:
        pass

    def buscar_funcionarios_por_cargo(self, cargo: CargoEnum) -> List[Funcionario]:
        pass

    def atualizar_funcionario(self, id_funcionario: int, nome: str = None,
                              cargo: CargoEnum = None, senha: str = None) -> Funcionario:
        pass

    def deletar_funcionario(self, id_funcionario: int) -> bool:
        pass

    def autenticar_funcionario(self, nome_usuario: str, senha: str) -> Optional[Funcionario]:
        pass

    def verificar_nome_usuario_existente(self, nome_usuario: str) -> bool:
        pass

    def criptografar_senha(self, senha: str) -> str:
        pass

    def verificar_senha(self, senha: str, senha_hash: str) -> bool:
        pass


class VendaServico:
    """Serviço para regras de negócio da entidade Venda."""

    def __init__(self):
        self.venda_repo = VendaRepositorio()
        self.itens_venda_repo = ItensVendaRepositorio()
        self.produto_Servico = ProdutoServico()

    def criar_venda(self, id_funcionario: int, id_cliente: int = None) -> Venda:
        pass

    def buscar_venda_por_id(self, id_venda: int) -> Optional[Venda]:
        pass

    def buscar_todas_vendas(self) -> List[Venda]:
        pass

    def buscar_vendas_por_funcionario(self, id_funcionario: int) -> List[Venda]:
        pass

    def buscar_vendas_por_cliente(self, id_cliente: int) -> List[Venda]:
        pass

    def buscar_vendas_por_periodo(self, data_inicio: datetime, data_fim: datetime) -> List[Venda]:
        pass

    def finalizar_venda(self, id_venda: int) -> Venda:
        pass

    def cancelar_venda(self, id_venda: int) -> bool:
        pass

    def calcular_valor_total_venda(self, id_venda: int) -> float:
        pass

    def adicionar_item_venda(self, id_venda: int, id_produto: int, quantidade: int,
                             desconto_aplicado: float = 0.0) -> ItensVenda:
        pass

    def remover_item_venda(self, id_item_venda: int) -> bool:
        pass


class ItensVendaServico:
    """Serviço para regras de negócio da entidade ItensVenda."""

    def __init__(self):
        self.itens_venda_repo = ItensVendaRepositorio()
        self.produto_Servico = ProdutoServico()

    def criar_item_venda(self, id_venda: int, id_produto: int, quantidade: int,
                         preco_unitario: float, desconto_aplicado: float = 0.0) -> ItensVenda:
        pass

    def buscar_item_venda_por_id(self, id_item_venda: int) -> Optional[ItensVenda]:
        pass

    def buscar_itens_por_venda(self, id_venda: int) -> List[ItensVenda]:
        pass

    def buscar_itens_por_produto(self, id_produto: int) -> List[ItensVenda]:
        pass

    def atualizar_item_venda(self, id_item_venda: int, quantidade: int = None,
                             desconto_aplicado: float = None) -> ItensVenda:
        pass

    def deletar_item_venda(self, id_item_venda: int) -> bool:
        pass

    def calcular_subtotal(self, id_item_venda: int) -> float:
        pass

    def calcular_subtotal_com_desconto(self, quantidade: int, preco_unitario: float,
                                       desconto_aplicado: float) -> float:
        pass

    def validar_quantidade_disponivel(self, id_produto: int, quantidade: int) -> bool:
        pass

    def aplicar_desconto(self, id_item_venda: int, percentual_desconto: float) -> ItensVenda:
        pass
