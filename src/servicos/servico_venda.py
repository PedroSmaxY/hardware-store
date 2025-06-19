import datetime
from typing import List, Optional
from src.modelos.tabelas_bd import Venda, ItensVenda
from src.servicos.servico_produto import ProdutoServico
from src.repositorios.repositorio_itens_venda import ItensVendaRepositorio
from src.repositorios.repositorio_venda import VendaRepositorio

"""
Este arquivo implementa o serviço para operações de negócio da entidade Venda,
seguindo o padrão Service Layer. Encapsula todas as regras de negócio relacionadas
ao processamento de vendas, cálculo de valores totais, aplicação de descontos
e controle de transações, fornecendo uma camada de abstração entre a lógica
de negócio e o acesso aos dados da aplicação.
"""


class VendaServico:
    """Serviço para regras de negócio da entidade Venda."""

    def __init__(self):
        self.venda_repo = VendaRepositorio()
        self.itens_venda_repo = ItensVendaRepositorio()
        self.produto_servico = ProdutoServico()

    def criar_venda(self, id_funcionario: int, id_cliente: int = None) -> Venda:
        """RF05 - Registro de Venda"""
        if id_funcionario <= 0:
            raise Exception(
                "ID do funcionário deve ser maior que zero")

        venda = Venda(
            id_funcionario=id_funcionario,
            id_cliente=id_cliente,
            data_venda=datetime.now(),
            valor_total=0.0,
            desconto_aplicado=0.0
        )

        return self.venda_repo.salvar(venda)

    def buscar_venda_por_id(self, id_venda: int) -> Optional[Venda]:
        if id_venda <= 0:
            raise Exception(
                "ID da venda deve ser maior que zero")

        return self.venda_repo.buscar_por_id(id_venda)

    def buscar_todas_vendas(self) -> List[Venda]:
        return self.venda_repo.buscar_todos()

    def buscar_vendas_por_funcionario(self, id_funcionario: int) -> List[Venda]:
        if id_funcionario <= 0:
            raise Exception(
                "ID do funcionário deve ser maior que zero")

        return self.venda_repo.buscar_por_funcionario(id_funcionario)

    def buscar_vendas_por_cliente(self, id_cliente: int) -> List[Venda]:
        if id_cliente <= 0:
            raise Exception(
                "ID do cliente deve ser maior que zero")

        return self.venda_repo.buscar_por_cliente(id_cliente)

    def buscar_vendas_por_periodo(self, data_inicio: datetime, data_fim: datetime) -> List[Venda]:
        if data_inicio > data_fim:
            raise Exception(
                "Data de início deve ser anterior à data de fim")

        return self.venda_repo.buscar_por_periodo(data_inicio, data_fim)

    def finalizar_venda(self, id_venda: int) -> Venda:
        """RF13 - Processamento de Pagamento"""
        venda = self.venda_repo.buscar_por_id(id_venda)
        if not venda:
            raise Exception(
                f"Venda com ID {id_venda} não encontrada")

        # Calcula valor total
        valor_total = self.calcular_valor_total_venda(id_venda)
        venda.valor_total = valor_total

        # Aplica desconto se cliente cadastrado (RN02)
        if venda.id_cliente:
            desconto = min(valor_total * 0.05, valor_total *
                           0.10)  # máximo 10% (RN06)
            venda.desconto_aplicado = desconto
            venda.valor_total = valor_total - desconto

        return self.venda_repo.atualizar(venda)

    def cancelar_venda(self, id_venda: int) -> bool:
        """Cancela uma venda e retorna produtos ao estoque"""
        venda = self.venda_repo.buscar_por_id(id_venda)
        if not venda:
            raise Exception(
                f"Venda com ID {id_venda} não encontrada")

        # Retorna produtos ao estoque
        itens = self.itens_venda_repo.buscar_por_venda(id_venda)
        for item in itens:
            produto = self.produto_servico.buscar_produto_por_id(
                item.id_produto)
            if produto:
                produto.quantidade_estoque += item.quantidade
                self.produto_servico.produto_repo.atualizar(produto)

        return self.venda_repo.deletar(id_venda)

    def calcular_valor_total_venda(self, id_venda: int) -> float:
        """Calcula o valor total da venda baseado nos itens"""
        itens = self.itens_venda_repo.buscar_por_venda(id_venda)
        return sum(item.quantidade * item.preco_unitario - item.desconto_aplicado for item in itens)

    def adicionar_item_venda(self, id_venda: int, id_produto: int, quantidade: int,
                             desconto_aplicado: float = 0.0) -> ItensVenda:
        """RF09 - Adicionar Itens ao Carrinho"""
        # Verifica se a venda existe
        venda = self.venda_repo.buscar_por_id(id_venda)
        if not venda:
            raise Exception(
                f"Venda com ID {id_venda} não encontrada")

        # Verifica estoque disponível (RN03)
        if not self.produto_servico.verificar_estoque_disponivel(id_produto, quantidade):
            raise Exception(
                "Estoque insuficiente para a quantidade solicitada")

        produto = self.produto_servico.buscar_produto_por_id(id_produto)
        if not produto:
            raise Exception(
                f"Produto com ID {id_produto} não encontrado")

        # Valida desconto (RN06)
        if desconto_aplicado > produto.preco * quantidade * 0.10:
            raise Exception(
                "Desconto não pode exceder 10% do valor do item")

        item_venda = ItensVenda(
            id_venda=id_venda,
            id_produto=id_produto,
            quantidade=quantidade,
            preco_unitario=produto.preco,
            desconto_aplicado=desconto_aplicado
        )

        return self.itens_venda_repo.salvar(item_venda)

    def remover_item_venda(self, id_item_venda: int) -> bool:
        """RF10 - Remover Itens do Carrinho"""
        item = self.itens_venda_repo.buscar_por_id(id_item_venda)
        if not item:
            raise Exception(
                f"Item de venda com ID {id_item_venda} não encontrado")

        return self.itens_venda_repo.deletar(id_item_venda)
