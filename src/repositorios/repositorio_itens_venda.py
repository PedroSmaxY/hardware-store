from typing import List, Optional
from sqlalchemy.orm import Session
from src.configs.config_bd import Session as SessionLocal
from src.modelos.tabelas_bd import ItensVenda


class ItensVendaRepositorio:
    """Repositório para operações CRUD da entidade ItensVenda."""

    def __init__(self, session: Session | None = None):
        self.session = session or SessionLocal()

    def criar(self, item_venda: ItensVenda) -> ItensVenda:
        """Cria um novo item de venda no banco de dados."""
        try:
            self.session.add(item_venda)
            self.session.commit()
            self.session.refresh(item_venda)
            return item_venda
        except Exception as e:
            self.session.rollback()
            raise e

    def buscar_por_id(self, id_item_venda: int) -> Optional[ItensVenda]:
        """Busca um item de venda pelo ID."""
        return self.session.query(ItensVenda).filter(ItensVenda.id == id_item_venda).first()

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

    def calcular_subtotal(self, id_item_venda: int) -> float:
        """Calcula o subtotal de um item de venda (quantidade x preço unitário)."""
        item = self.buscar_por_id(id_item_venda)
        if item:
            return float(item.quantidade * item.preco_unitario)
        return 0.0
