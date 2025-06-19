from typing import List, Optional
from src.servicos.servico_produto import ProdutoServico
from src.repositorios.repositorio_itens_venda import ItensVendaRepositorio
from src.modelos.tabelas_bd import ItensVenda

"""
Este arquivo implementa o serviço para operações de negócio da entidade ItensVenda,
seguindo o padrão Service Layer. Encapsula todas as regras de negócio relacionadas
ao gerenciamento de itens individuais de vendas, cálculo de subtotais, aplicação
de descontos e validação de estoque, fornecendo uma camada de abstração entre
a lógica de negócio e o acesso aos dados da aplicação.
"""


class ItensVendaServico:
    """Serviço para regras de negócio da entidade ItensVenda."""

    def __init__(self):
        self.itens_venda_repo = ItensVendaRepositorio()
        self.produto_servico = ProdutoServico()

    def criar_item_venda(self, id_venda: int, id_produto: int, quantidade: int,
                         preco_unitario: float, desconto_aplicado: float = 0.0) -> ItensVenda:
        # Validações
        if quantidade <= 0:
            raise Exception("Quantidade deve ser maior que zero")

        if preco_unitario <= 0:
            raise Exception(
                "Preço unitário deve ser maior que zero")

        if desconto_aplicado < 0:
            raise Exception("Desconto não pode ser negativo")

        # Verifica estoque (RN03)
        if not self.validar_quantidade_disponivel(id_produto, quantidade):
            raise Exception("Estoque insuficiente")

        item_venda = ItensVenda(
            id_venda=id_venda,
            id_produto=id_produto,
            quantidade=quantidade,
            preco_unitario=preco_unitario,
            desconto_aplicado=desconto_aplicado
        )

        return self.itens_venda_repo.salvar(item_venda)

    def buscar_item_venda_por_id(self, id_item_venda: int) -> Optional[ItensVenda]:
        if id_item_venda <= 0:
            raise Exception(
                "ID do item de venda deve ser maior que zero")

        return self.itens_venda_repo.buscar_por_id(id_item_venda)

    def buscar_itens_por_venda(self, id_venda: int) -> List[ItensVenda]:
        """RF12 - Visualizar Carrinho"""
        if id_venda <= 0:
            raise Exception(
                "ID da venda deve ser maior que zero")

        return self.itens_venda_repo.buscar_por_venda(id_venda)

    def buscar_itens_por_produto(self, id_produto: int) -> List[ItensVenda]:
        if id_produto <= 0:
            raise Exception(
                "ID do produto deve ser maior que zero")

        return self.itens_venda_repo.buscar_por_produto(id_produto)

    def atualizar_item_venda(self, id_item_venda: int, quantidade: int = None,
                             desconto_aplicado: float = None) -> ItensVenda:
        """RF11 - Ajustar Quantidade de Itens no Carrinho"""
        item = self.itens_venda_repo.buscar_por_id(id_item_venda)
        if not item:
            raise Exception(
                f"Item de venda com ID {id_item_venda} não encontrado")

        if quantidade is not None:
            if quantidade <= 0:
                raise Exception(
                    "Quantidade deve ser maior que zero")

            if not self.validar_quantidade_disponivel(item.id_produto, quantidade):
                raise Exception(
                    "Estoque insuficiente para a nova quantidade")

            item.quantidade = quantidade

        if desconto_aplicado is not None:
            if desconto_aplicado < 0:
                raise Exception("Desconto não pode ser negativo")

            # Valida limite de desconto (RN06)
            valor_item = item.quantidade * item.preco_unitario
            if desconto_aplicado > valor_item * 0.10:
                raise Exception(
                    "Desconto não pode exceder 10% do valor do item")

            item.desconto_aplicado = desconto_aplicado

        return self.itens_venda_repo.atualizar(item)

    def deletar_item_venda(self, id_item_venda: int) -> bool:
        item = self.itens_venda_repo.buscar_por_id(id_item_venda)
        if not item:
            raise Exception(
                f"Item de venda com ID {id_item_venda} não encontrado")

        return self.itens_venda_repo.deletar(id_item_venda)

    def calcular_subtotal(self, id_item_venda: int) -> float:
        """Calcula o subtotal de um item de venda"""
        item = self.itens_venda_repo.buscar_por_id(id_item_venda)
        if not item:
            raise Exception(
                f"Item de venda com ID {id_item_venda} não encontrado")

        return self.calcular_subtotal_com_desconto(
            item.quantidade,
            item.preco_unitario,
            item.desconto_aplicado
        )

    def calcular_subtotal_com_desconto(self, quantidade: int, preco_unitario: float,
                                       desconto_aplicado: float) -> float:
        """Calcula subtotal com desconto aplicado"""
        subtotal_bruto = quantidade * preco_unitario
        return subtotal_bruto - desconto_aplicado

    def validar_quantidade_disponivel(self, id_produto: int, quantidade: int) -> bool:
        """RN03 - Controle de Estoque"""
        return self.produto_servico.verificar_estoque_disponivel(id_produto, quantidade)

    def aplicar_desconto(self, id_item_venda: int, percentual_desconto: float) -> ItensVenda:
        """RF07 - Aplicação de Descontos"""
        if percentual_desconto < 0 or percentual_desconto > 10:
            raise Exception(
                "Percentual de desconto deve estar entre 0% e 10%")

        item = self.itens_venda_repo.buscar_por_id(id_item_venda)
        if not item:
            raise Exception(
                f"Item de venda com ID {id_item_venda} não encontrado")

        valor_item = item.quantidade * item.preco_unitario
        desconto = valor_item * (percentual_desconto / 100)

        item.desconto_aplicado = desconto
        return self.itens_venda_repo.atualizar(item)
