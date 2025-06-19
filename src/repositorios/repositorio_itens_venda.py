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

    def salvar(self, item_venda: ItensVenda) -> ItensVenda:
        """Salva um item de venda no banco de dados."""
        try:
            self.session.add(item_venda)
            self.session.commit()
            self.session.refresh(item_venda)
            return item_venda
        except Exception as e:
            self.session.rollback()
            raise e

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

    def atualizar(self, item_venda: ItensVenda) -> ItensVenda:
        """Atualiza um item de venda existente."""
        try:
            self.session.merge(item_venda)
            self.session.commit()
            return item_venda
        except Exception as e:
            self.session.rollback()
            raise e

    def atualizar_por_id(self, id_item_venda: int, id_venda: Optional[int] = None, id_produto: Optional[int] = None,
                         quantidade: Optional[int] = None, preco_unitario: Optional[float] = None,
                         desconto_aplicado: Optional[float] = None) -> Optional[ItensVenda]:
        """Atualiza um item de venda existente por ID."""
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

    def buscar_todos(self) -> List[ItensVenda]:
        """Busca todos os itens de venda."""
        return self.session.query(ItensVenda).all()

    def buscar_com_desconto(self) -> List[ItensVenda]:
        """Busca itens de venda que tiveram desconto aplicado."""
        return self.session.query(ItensVenda).filter(
            ItensVenda.desconto_aplicado > 0
        ).all()

    def calcular_total_descontos_venda(self, id_venda: int) -> float:
        """Calcula o total de descontos aplicados em uma venda."""
        resultado = self.session.query(
            func.sum(func.coalesce(ItensVenda.desconto_aplicado, 0))
        ).filter(ItensVenda.id_venda == id_venda).scalar()

        return float(resultado) if resultado else 0.0

    def buscar_itens_por_preco_range(self, preco_minimo: float, preco_maximo: float) -> List[ItensVenda]:
        """Busca itens de venda dentro de uma faixa de preço unitário."""
        return self.session.query(ItensVenda).filter(
            ItensVenda.preco_unitario >= preco_minimo,
            ItensVenda.preco_unitario <= preco_maximo
        ).all()

    def buscar_produtos_mais_vendidos(self, limite: int = 10) -> List[dict]:
        """Busca os produtos mais vendidos baseado na quantidade de itens vendidos."""
        resultado = self.session.query(
            ItensVenda.id_produto,
            func.sum(ItensVenda.quantidade).label('total_vendido'),
            func.count(ItensVenda.id_item_venda).label('numero_vendas')
        ).group_by(ItensVenda.id_produto).order_by(
            func.sum(ItensVenda.quantidade).desc()
        ).limit(limite).all()

        return [
            {
                "id_produto": r.id_produto,
                "total_vendido": r.total_vendido,
                "numero_vendas": r.numero_vendas
            }
            for r in resultado
        ]

    def fechar_sessao(self):
        """Fecha a sessão do banco de dados."""
        self.session.close()
