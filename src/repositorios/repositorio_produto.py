from typing import List, Optional
from sqlalchemy.orm import Session
from src.configs.config_bd import Session as SessionLocal
from src.modelos.tabelas_bd import Produto


class ProdutoRepositorio:
    """Repositório para operações CRUD da entidade Produto."""

    def __init__(self, session: Session | None = None):
        self.session = session or SessionLocal()

    def criar(self, produto: Produto) -> Produto:
        """Cria um novo produto no banco de dados."""
        try:
            self.session.add(produto)
            self.session.commit()
            self.session.refresh(produto)
            return produto
        except Exception as e:
            self.session.rollback()
            raise e

    def buscar_por_id(self, id_produto: int) -> Optional[Produto]:
        """Busca um produto pelo ID."""
        return self.session.query(Produto).filter(Produto.id == id_produto).first()

    def buscar_todos(self) -> List[Produto]:
        """Retorna todos os produtos cadastrados."""
        return self.session.query(Produto).all()

    def buscar_por_nome(self, nome: str) -> List[Produto]:
        """Busca produtos pelo nome (busca parcial)."""
        return self.session.query(Produto).filter(
            Produto.nome.ilike(f"%{nome}%")
        ).all()

    def atualizar(self, produto: Produto) -> Produto:
        """Atualiza um produto existente."""
        try:
            self.session.merge(produto)
            self.session.commit()
            return produto
        except Exception as e:
            self.session.rollback()
            raise e

    def deletar(self, id_produto: int) -> bool:
        """Deleta um produto pelo ID."""
        try:
            produto = self.buscar_por_id(id_produto)
            if produto:
                self.session.delete(produto)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def atualizar_estoque(self, id_produto: int, nova_quantidade: int) -> bool:
        """Atualiza a quantidade em estoque de um produto."""
        try:
            produto = self.buscar_por_id(id_produto)
            if produto:
                produto.quantidade_estoque = nova_quantidade
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e
