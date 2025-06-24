from datetime import datetime
from decimal import Decimal
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

    def criar_venda(self, id_funcionario: int, id_cliente: int = None, persistir: bool = True) -> Venda:
        if id_funcionario <= 0:
            raise Exception("ID do funcionário deve ser maior que zero")

        venda = Venda(
            id_funcionario=id_funcionario,
            id_cliente=id_cliente,
            data_venda=datetime.now()
        )

        return self.venda_repo.salvar(venda) if persistir else venda

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
            raise Exception(f"Venda com ID {id_venda} não encontrada")

        # Apenas aplica desconto se cliente cadastrado (RN02)
        if venda.id_cliente:
            pass

        return venda

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
                             percentual_desconto: float = 0.0) -> ItensVenda:
        """RF09 - Adicionar Itens ao Carrinho"""

        # Verifica se a venda existe
        venda = self.venda_repo.buscar_por_id(id_venda)
        if not venda:
            raise Exception(f"Venda com ID {id_venda} não encontrada")

        # Verifica estoque disponível (RN03)
        if not self.produto_servico.verificar_estoque_disponivel(id_produto, quantidade):
            raise Exception(
                "Estoque insuficiente para a quantidade solicitada")

        produto = self.produto_servico.buscar_produto_por_id(id_produto)
        if not produto:
            raise Exception(f"Produto com ID {id_produto} não encontrado")

        # Aplicar desconto automático para clientes cadastrados (RN02)
        if venda.id_cliente and percentual_desconto == 0.0:
            percentual_desconto = 5.0  # 5% para clientes cadastrados

        # Valida percentual de desconto (RN06)
        if percentual_desconto < 0 or percentual_desconto > 10:
            raise Exception("Percentual de desconto deve estar entre 0% e 10%")

        # Calcula o valor do desconto
        valor_item = float(produto.preco) * quantidade
        desconto_aplicado = valor_item * (percentual_desconto / 100)

        item_venda = ItensVenda(
            id_venda=id_venda,
            id_produto=id_produto,
            quantidade=quantidade,
            preco_unitario=float(produto.preco),
            desconto_aplicado=desconto_aplicado
        )

        # Salva o item
        item_salvo = self.itens_venda_repo.salvar(item_venda)

        # Atualiza os totais da venda
        self._sincronizar_totais_venda(id_venda)

        # Reduz o estoque do produto
        self.produto_servico.reduzir_estoque(id_produto, quantidade)

        return item_salvo

    def remover_item_venda(self, id_item_venda: int) -> bool:
        """RF10 - Remover Itens do Carrinho"""
        item = self.itens_venda_repo.buscar_por_id(id_item_venda)
        if not item:
            raise Exception(
                f"Item de venda com ID {id_item_venda} não encontrado")

        id_venda = item.id_venda

        # Remove o item
        sucesso = self.itens_venda_repo.deletar(id_item_venda)

        if sucesso:
            self.produto_servico.produto_repo.aumentar_estoque(
                item.id_produto, item.quantidade)

            self._sincronizar_totais_venda(id_venda)

        return sucesso

    def _sincronizar_totais_venda(self, id_venda: int):
        """Recalcula e atualiza os totais da venda no banco."""
        itens = self.itens_venda_repo.buscar_por_venda(id_venda)

        valor_total = 0.0
        desconto_total = 0.0

        for item in itens:
            valor_bruto = float(item.quantidade * item.preco_unitario)
            desconto_item = float(item.desconto_aplicado or 0.0)

            valor_total += (valor_bruto - desconto_item)
            desconto_total += desconto_item

        self.venda_repo.atualizar_totais_venda(
            id_venda, valor_total, desconto_total)

    def calcular_valor_total_venda(self, id_venda: int) -> float:
        """Calcula o valor total da venda, incluindo descontos aplicados."""
        venda = self.venda_repo.buscar_por_id(id_venda)
        return float(venda.valor_total) if venda else 0.0

    def finalizar_venda(self, id_venda: int) -> Venda:
        """RF13 - Processamento de Pagamento"""
        venda = self.venda_repo.buscar_por_id(id_venda)
        if not venda:
            raise Exception(f"Venda com ID {id_venda} não encontrada")

        self._sincronizar_totais_venda(id_venda)

        return self.venda_repo.buscar_por_id(id_venda)
