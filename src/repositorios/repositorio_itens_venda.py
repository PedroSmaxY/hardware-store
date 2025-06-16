from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.configs.config_bd import Session as SessionLocal
from src.modelos.tabelas_bd import ItensVenda

"""
Este arquivo implementa o repositório para operações CRUD da entidade ItensVenda,
seguindo o padrão Repository. Encapsula todas as operações de acesso a dados
relacionadas aos itens de venda, fornecendo uma camada de abstração entre o modelo
de dados e a lógica de negócio da aplicação.
"""


class ItensVendaRepositorio:
    """Repositório para operações CRUD da entidade ItensVenda."""

    def __init__(self, session: Session | None = None):
        self.session = session or SessionLocal()

    def criar(self, id_venda: int, id_produto: int, quantidade: int = 1,
              preco_unitario: float = 0.0, desconto_aplicado: Optional[float] = 0.00) -> ItensVenda:
        """Cria um novo item de venda no banco de dados."""
        try:
            item_venda = ItensVenda(
                id_venda=id_venda,
                id_produto=id_produto,
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                desconto_aplicado=desconto_aplicado
            )
            self.session.add(item_venda)
            self.session.commit()
            self.session.refresh(item_venda)
            return item_venda
        except Exception as e:
            self.session.rollback()
            raise e

    def criar_multiplos(self, itens_venda: List[ItensVenda]) -> List[ItensVenda]:
        """Cria múltiplos itens de venda de uma só vez."""
        try:
            self.session.add_all(itens_venda)
            self.session.commit()
            for item in itens_venda:
                self.session.refresh(item)
            return itens_venda
        except Exception as e:
            self.session.rollback()
            raise e

    def buscar_por_id(self, id_item_venda: int) -> Optional[ItensVenda]:
        """Busca um item de venda pelo ID."""
        return self.session.query(ItensVenda).filter(ItensVenda.id_item_venda == id_item_venda).first()

    def buscar_por_venda(self, id_venda: int) -> List[ItensVenda]:
        """Busca todos os itens de uma venda específica."""
        return self.session.query(ItensVenda).filter(
            ItensVenda.id_venda == id_venda
        ).all()

    def buscar_por_produto(self, id_produto: int) -> List[ItensVenda]:
        """Busca todos os itens de venda de um produto específico."""
        return self.session.query(ItensVenda).filter(
            ItensVenda.id_produto == id_produto
        ).all()

    def atualizar(self, id_item_venda: int, id_venda: Optional[int] = None, id_produto: Optional[int] = None,
                  quantidade: Optional[int] = None, preco_unitario: Optional[float] = None,
                  desconto_aplicado: Optional[float] = None) -> Optional[ItensVenda]:
        """Atualiza um item de venda existente."""
        try:
            item_venda = self.buscar_por_id(id_item_venda)
            if item_venda:
                if id_venda is not None:
                    item_venda.id_venda = id_venda
                if id_produto is not None:
                    item_venda.id_produto = id_produto
                if quantidade is not None:
                    item_venda.quantidade = quantidade
                if preco_unitario is not None:
                    item_venda.preco_unitario = preco_unitario
                if desconto_aplicado is not None:
                    item_venda.desconto_aplicado = desconto_aplicado

                self.session.commit()
                return item_venda
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def deletar(self, id_item_venda: int) -> bool:
        """Deleta um item de venda pelo ID."""
        try:
            item_venda = self.buscar_por_id(id_item_venda)
            if item_venda:
                self.session.delete(item_venda)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def deletar_por_venda(self, id_venda: int) -> bool:
        """Deleta todos os itens de uma venda específica."""
        try:
            itens = self.buscar_por_venda(id_venda)
            for item in itens:
                self.session.delete(item)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    def calcular_subtotal(self, id_item_venda: int) -> float:
        """Calcula o subtotal de um item de venda (quantidade x preço unitário - desconto)."""
        item = self.buscar_por_id(id_item_venda)
        if item:
            subtotal = item.quantidade * item.preco_unitario
            desconto = item.desconto_aplicado or 0.0
            return float(subtotal - desconto)
        return 0.0

    def calcular_total_venda(self, id_venda: int) -> float:
        """Calcula o valor total de uma venda (soma de todos os itens)."""
        resultado = self.session.query(
            func.sum((ItensVenda.quantidade * ItensVenda.preco_unitario) -
                     func.coalesce(ItensVenda.desconto_aplicado, 0))
        ).filter(ItensVenda.id_venda == id_venda).scalar()

        return float(resultado) if resultado else 0.0

    def contar_itens_venda(self, id_venda: int) -> int:
        """Conta quantos itens uma venda possui."""
        return self.session.query(ItensVenda).filter(
            ItensVenda.id_venda == id_venda
        ).count()
