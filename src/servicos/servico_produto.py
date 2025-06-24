from typing import List, Optional
from datetime import datetime
from src.repositorios.repositorio_produto import ProdutoRepositorio
from src.modelos.tabelas_bd import Produto

"""
Este arquivo implementa o serviço para operações de negócio da entidade Produto,
seguindo o padrão Service Layer. Encapsula todas as regras de negócio relacionadas
ao gerenciamento de produtos e controle de estoque, fornecendo uma camada de
abstração entre a lógica de negócio e o acesso aos dados da aplicação.
"""


class ProdutoServico:
    """Serviço para regras de negócio da entidade Produto."""

    def __init__(self):
        self.produto_repo = ProdutoRepositorio()

    def criar_produto(self, nome: str, descricao: str, quantidade_estoque: int, preco: float) -> Produto:
        """
        Cria um novo produto no sistema.
        Validações: nome não pode ser vazio, quantidade >= 0, preço > 0
        """
        # Validação de dados (RN04)
        if not nome or nome.strip() == "":
            raise Exception("Nome do produto não pode ser vazio")

        if quantidade_estoque < 0:
            raise Exception(
                "Quantidade em estoque não pode ser negativa")

        if preco <= 0:
            raise Exception("Preço deve ser maior que zero")

        # Verifica se já existe produto com mesmo nome
        produtos_existentes = self.produto_repo.buscar_por_nome(nome.strip())
        if produtos_existentes:
            raise Exception(
                f"Já existe um produto com o nome '{nome}'")

        # Cria o produto
        produto = Produto(
            nome=nome.strip(),
            descricao=descricao.strip() if descricao else "",
            quantidade_estoque=quantidade_estoque,
            preco=preco
        )

        return self.produto_repo.salvar(produto)

    def buscar_produto_por_id(self, id_produto: int) -> Optional[Produto]:
        """Busca um produto pelo ID."""
        if id_produto <= 0:
            raise Exception(
                "ID do produto deve ser maior que zero")

        return self.produto_repo.buscar_por_id(id_produto)

    def buscar_todos_produtos(self) -> List[Produto]:
        """Retorna todos os produtos cadastrados."""
        return self.produto_repo.buscar_todos()

    def buscar_produtos_por_nome(self, nome: str) -> List[Produto]:
        """Busca produtos por nome (RF08 - Busca de Produtos)."""
        if not nome or nome.strip() == "":
            return []

        return self.produto_repo.buscar_por_nome(nome.strip())

    def atualizar_produto(self, id_produto: int, nome: str = None, descricao: str = None,
                          quantidade_estoque: int = None, preco: float = None) -> Produto:
        """
        Atualiza informações de um produto existente.
        Apenas gerentes podem editar produtos (RN01).
        """
        # Busca o produto
        produto = self.produto_repo.buscar_por_id(id_produto)
        if not produto:
            raise Exception(
                f"Produto com ID {id_produto} não encontrado")

        # Validações dos novos dados
        if nome is not None:
            if not nome or nome.strip() == "":
                raise Exception(
                    "Nome do produto não pode ser vazio")

            # Verifica se já existe outro produto com mesmo nome
            produtos_existentes = self.produto_repo.buscar_por_nome(
                nome.strip())
            if produtos_existentes and produtos_existentes[0].id_produto != id_produto:
                raise Exception(
                    f"Já existe outro produto com o nome '{nome}'")

            produto.nome = nome.strip()

        if descricao is not None:
            produto.descricao = descricao.strip()

        if quantidade_estoque is not None:
            if quantidade_estoque < 0:
                raise Exception(
                    "Quantidade em estoque não pode ser negativa")
            produto.quantidade_estoque = quantidade_estoque

        if preco is not None:
            if preco <= 0:
                raise Exception("Preço deve ser maior que zero")
            produto.preco = preco

        produto.data_atualizacao = datetime.now()
        return self.produto_repo.atualizar(produto)

    def deletar_produto(self, id_produto: int) -> bool:
        """
        Remove um produto do sistema.
        Apenas gerentes podem deletar produtos (RN01).
        """
        produto = self.produto_repo.buscar_por_id(id_produto)
        if not produto:
            raise Exception(
                f"Produto com ID {id_produto} não encontrado")

        return self.produto_repo.deletar(id_produto)

    def verificar_estoque_disponivel(self, id_produto: int, quantidade_solicitada: int) -> bool:
        """
        Verifica se há estoque suficiente para uma venda (RN03).
        """
        if quantidade_solicitada <= 0:
            raise Exception(
                "Quantidade solicitada deve ser maior que zero")

        produto = self.produto_repo.buscar_por_id(id_produto)
        if not produto:
            raise Exception(
                f"Produto com ID {id_produto} não encontrado")

        return produto.quantidade_estoque >= quantidade_solicitada

    def atualizar_estoque(self, id_produto: int, nova_quantidade: int) -> bool:
        """
        Atualiza a quantidade em estoque de um produto.
        Apenas estoquistas e gerentes podem fazer isso.
        """
        if nova_quantidade < 0:
            raise Exception(
                "Nova quantidade não pode ser negativa")

        produto = self.produto_repo.buscar_por_id(id_produto)
        if not produto:
            raise Exception(
                f"Produto com ID {id_produto} não encontrado")

        produto.quantidade_estoque = nova_quantidade
        produto.data_atualizacao = datetime.now()

        produto_atualizado = self.produto_repo.atualizar(produto)
        return produto_atualizado is not None

    def reduzir_estoque(self, id_produto: int, quantidade: int) -> bool:
        """
        Reduz o estoque após uma venda (RF05).
        Implementa controle de estoque (RN03).
        """
        if quantidade <= 0:
            raise Exception(
                "Quantidade a reduzir deve ser maior que zero")

        produto = self.produto_repo.buscar_por_id(id_produto)
        if not produto:
            raise Exception(
                f"Produto com ID {id_produto} não encontrado")

        # Verifica se há estoque suficiente (RN03)
        if produto.quantidade_estoque < quantidade:
            raise Exception(
                f"Estoque insuficiente. Disponível: {produto.quantidade_estoque}, "
                f"Solicitado: {quantidade}"
            )

        # Reduz o estoque
        produto.quantidade_estoque -= quantidade
        produto.data_atualizacao = datetime.now()

        produto_atualizado = self.produto_repo.atualizar(produto)
        return produto_atualizado is not None

    def adicionar_estoque(self, id_produto: int, quantidade: int) -> bool:
        """
        Adiciona quantidade ao estoque existente.
        Útil para reposição de produtos.
        """
        if quantidade <= 0:
            raise Exception(
                "Quantidade a adicionar deve ser maior que zero")

        produto = self.produto_repo.buscar_por_id(id_produto)
        if not produto:
            raise Exception(
                f"Produto com ID {id_produto} não encontrado")

        produto.quantidade_estoque += quantidade
        produto.data_atualizacao = datetime.now()

        produto_atualizado = self.produto_repo.atualizar(produto)
        return produto_atualizado is not None

    def buscar_produtos_em_falta(self, limite_minimo: int = 5) -> List[Produto]:
        """
        Retorna produtos com estoque baixo para relatórios (RF04).
        """
        todos_produtos = self.produto_repo.buscar_todos()
        return [p for p in todos_produtos if p.quantidade_estoque <= limite_minimo]

    def gerar_relatorio_estoque(self) -> dict:
        """
        Gera relatório básico de estoque (RF04).
        """
        produtos = self.produto_repo.buscar_todos()

        total_produtos = len(produtos)
        total_itens_estoque = sum(p.quantidade_estoque for p in produtos)
        valor_total_estoque = sum(
            p.quantidade_estoque * p.preco for p in produtos)
        produtos_em_falta = len(self.buscar_produtos_em_falta())

        return {
            "total_produtos_cadastrados": total_produtos,
            "total_itens_em_estoque": total_itens_estoque,
            "valor_total_estoque": valor_total_estoque,
            "produtos_com_estoque_baixo": produtos_em_falta,
            "data_relatorio": datetime.now().isoformat()
        }
