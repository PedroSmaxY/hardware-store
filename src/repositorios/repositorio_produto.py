from typing import List, Optional
from sqlalchemy.orm import Session
from src.configs.config_bd import Session as SessionLocal
from src.modelos.tabelas_bd import Produto

"""
Este arquivo implementa o repositório para operações CRUD da entidade Produto,
seguindo o padrão Repository. Encapsula todas as operações de acesso a dados
relacionadas aos produtos, fornecendo uma camada de abstração entre o modelo
de dados e a lógica de negócio da aplicação.
"""


class ProdutoRepositorio:
    """Repositório para operações CRUD da entidade Produto."""

    def __init__(self, session: Session | None = None):
        self.session = session or SessionLocal()

    def salvar(self, produto: Produto) -> Produto:
        """Salva um produto no banco de dados."""
        try:
            self.session.add(produto)
            self.session.commit()
            self.session.refresh(produto)
            return produto
        except Exception as e:
            self.session.rollback()
            raise e

    def criar(self, nome: str, preco: float, descricao: Optional[str] = None,
              quantidade_estoque: int = 0) -> Produto:
        """Cria um novo produto no banco de dados."""
        try:
            produto = Produto(
                nome=nome,
                preco=preco,
                descricao=descricao,
                quantidade_estoque=quantidade_estoque
            )
            self.session.add(produto)
            self.session.commit()
            self.session.refresh(produto)
            return produto
        except Exception as e:
            self.session.rollback()
            raise e

    def buscar_por_id(self, id_produto: int) -> Optional[Produto]:
        """Busca um produto pelo ID."""
        return self.session.query(Produto).filter(Produto.id_produto == id_produto).first()

    def buscar_todos(self) -> List[Produto]:
        """Retorna todos os produtos cadastrados."""
        return self.session.query(Produto).all()

    def buscar_por_nome(self, nome: str) -> List[Produto]:
        """Busca produtos pelo nome (busca parcial)."""
        return self.session.query(Produto).filter(
            Produto.nome.ilike(f"%{nome}%")
        ).all()

    def buscar_com_estoque_baixo(self, limite: int = 10) -> List[Produto]:
        """Busca produtos com estoque baixo."""
        return self.session.query(Produto).filter(
            Produto.quantidade_estoque <= limite
        ).all()

    def buscar_sem_estoque(self) -> List[Produto]:
        """Busca produtos sem estoque."""
        return self.session.query(Produto).filter(
            Produto.quantidade_estoque == 0
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

    def atualizar_por_id(self, id_produto: int, nome: Optional[str] = None, preco: Optional[float] = None,
                         descricao: Optional[str] = None, quantidade_estoque: Optional[int] = None) -> Optional[Produto]:
        """Atualiza um produto existente por ID."""
        try:
            produto = self.buscar_por_id(id_produto)
            if produto:
                if nome is not None:
                    produto.nome = nome
                if preco is not None:
                    produto.preco = preco
                if descricao is not None:
                    produto.descricao = descricao
                if quantidade_estoque is not None:
                    produto.quantidade_estoque = quantidade_estoque

                self.session.commit()
                return produto
            return None
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

    def reduzir_estoque(self, id_produto: int, quantidade: int) -> bool:
        """Reduz o estoque de um produto."""
        try:
            produto = self.buscar_por_id(id_produto)
            if produto and produto.quantidade_estoque >= quantidade:
                produto.quantidade_estoque -= quantidade
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def aumentar_estoque(self, id_produto: int, quantidade: int) -> bool:
        """Aumenta o estoque de um produto."""
        try:
            produto = self.buscar_por_id(id_produto)
            if produto:
                produto.quantidade_estoque += quantidade
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def verificar_estoque_disponivel(self, id_produto: int, quantidade_desejada: int) -> bool:
        """Verifica se há estoque suficiente para uma quantidade desejada."""
        produto = self.buscar_por_id(id_produto)
        if produto:
            return produto.quantidade_estoque >= quantidade_desejada
        return False

    def buscar_por_preco_range(self, preco_minimo: float, preco_maximo: float) -> List[Produto]:
        """Busca produtos dentro de uma faixa de preço."""
        return self.session.query(Produto).filter(
            Produto.preco >= preco_minimo,
            Produto.preco <= preco_maximo
        ).all()

    def buscar_ordenado_por_preco(self, crescente: bool = True) -> List[Produto]:
        """Busca produtos ordenados por preço."""
        if crescente:
            return self.session.query(Produto).order_by(Produto.preco.asc()).all()
        else:
            return self.session.query(Produto).order_by(Produto.preco.desc()).all()

    def buscar_ordenado_por_nome(self) -> List[Produto]:
        """Busca produtos ordenados por nome."""
        return self.session.query(Produto).order_by(Produto.nome.asc()).all()

    def contar_produtos(self) -> int:
        """Conta o total de produtos cadastrados."""
        return self.session.query(Produto).count()

    def calcular_valor_total_estoque(self) -> float:
        """Calcula o valor total do estoque."""
        produtos = self.buscar_todos()
        return sum(produto.quantidade_estoque * produto.preco for produto in produtos)

    def verificar_nome_existe(self, nome: str, id_produto: Optional[int] = None) -> bool:
        """Verifica se um nome de produto já existe no banco (exceto para o próprio produto)."""
        query = self.session.query(Produto).filter(Produto.nome == nome)
        if id_produto:
            query = query.filter(Produto.id_produto != id_produto)
        return query.first() is not None

    def fechar_sessao(self):
        """Fecha a sessão do banco de dados."""
        self.session.close()
