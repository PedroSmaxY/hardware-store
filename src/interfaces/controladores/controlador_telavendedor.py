from decimal import Decimal
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt, QAbstractTableModel
from src.modelos.tabelas_bd import Produto
from src.servicos.servico_produto import ProdutoServico
from src.servicos.servico_cliente import ClienteServico
from src.servicos.servico_itens_venda import ItensVendaServico


class SimpleTableModel(QAbstractTableModel):
    """
    Modelo de tabela simples para exibição de listas genéricas,
    com suporte a atualização dos dados e alteração visual da quantidade de produtos.
    """
    def __init__(self, data: list, columns: list, row_to_values_func):
        super().__init__()
        self._data = data
        self._columns = columns
        self._row_to_values = row_to_values_func

    def rowCount(self, parent=None) -> int:
        return len(self._data)

    def columnCount(self, parent=None) -> int:
        return len(self._columns)

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        row_obj = self._data[index.row()]
        return self._row_to_values(row_obj)[index.column()]

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._columns[section]

    def atualizar_dados(self, novos_dados: list):
        self.beginResetModel()
        self._data = novos_dados
        self.endResetModel()

    def atualizar_quantidade_produto(self, id_produto: int, delta: int):
        """
        Atualiza a quantidade visual do produto pelo delta fornecido (positivo ou negativo)
        e emite o sinal para atualização da view.
        """
        for produto in self._data:
            if produto.id_produto == id_produto:
                produto.quantidade_estoque += delta
                linha = self._data.index(produto)
                topo_esquerda = self.createIndex(linha, 0)
                fundo_direita = self.createIndex(linha, len(self._columns) - 1)
                self.dataChanged.emit(topo_esquerda, fundo_direita, [Qt.ItemDataRole.DisplayRole])
                break


class ControladorTelaVendedor:
    """
    Controlador da tela de vendas.
    Gerencia interações entre UI, modelos, carrinho local e serviços.
    """
    DESCONTO_CLIENTE = Decimal("0.05")  # 5% de desconto para clientes

    def __init__(self, id_funcionario: int):
        self.id_funcionario = id_funcionario
        self.produto_servico = ProdutoServico()
        self.cliente_servico = ClienteServico()
        self.itens_venda_servico = ItensVendaServico()

        # Carrinho local mapeia {id_produto: quantidade}
        self.carrinho_local = {}

        # Interface carregada via arquivo .ui
        self.dialog = uic.loadUi("src/interfaces/telas/Menu_Vendas.ui")

        # Conectar sinais dos botões
        self.dialog.button_adicionarItemCarrinho.clicked.connect(self.adicionar_item)
        self.dialog.button_excluirItemCarrinho.clicked.connect(self.remover_item)
        self.dialog.button_concluirCompra.clicked.connect(self.concluir_compra)
        self.dialog.pushButton.clicked.connect(self.deslogar)

        # Configuração das tabelas para seleção por linha
        self.dialog.table_produtos.setSelectionBehavior(self.dialog.table_produtos.SelectionBehavior.SelectRows)
        self.dialog.table_carrinho.setSelectionBehavior(self.dialog.table_carrinho.SelectionBehavior.SelectRows)

        # Inicialização dos modelos de dados para as tabelas
        self.modelo_produtos = SimpleTableModel(
            [],
            ["ID", "Nome", "Preço", "Estoque"],
            row_to_values_func=lambda p: [p.id_produto, p.nome, f"R$ {p.preco:.2f}", p.quantidade_estoque]
        )
        self.modelo_carrinho = SimpleTableModel(
            [],
            ["Produto", "Qtd", "Unitário", "Desconto"],
            row_to_values_func=lambda i: [
                self.produto_servico.buscar_produto_por_id(i.id_produto).nome if i.id_produto else "Produto Desconhecido",
                i.quantidade,
                f"R$ {i.preco_unitario:.2f}",
                f"R$ {i.desconto_aplicado:.2f}"
            ]
        )
        self.dialog.table_produtos.setModel(self.modelo_produtos)
        self.dialog.table_carrinho.setModel(self.modelo_carrinho)

        self.carregar_produtos()
        self.carregar_clientes()
        self.dialog.comboBox_clientes.currentIndexChanged.connect(self.atualizar_carrinho_local)


    def executar(self):
        """
        Executa o diálogo modal da tela de vendas.
        """
        return self.dialog.exec()

    def carregar_produtos(self):
        """
        Busca todos os produtos do banco e atualiza o modelo da tabela de produtos.
        """
        produtos = self.produto_servico.buscar_todos_produtos()
        self.modelo_produtos.atualizar_dados(produtos)

    def carregar_clientes(self):
        """
        Busca todos os clientes do banco e popula o combobox de seleção de clientes,
        incluindo a opção 'Sem Cliente'.
        """
        clientes = self.cliente_servico.buscar_todos_clientes()
        self.dialog.comboBox_clientes.clear()
        self.dialog.comboBox_clientes.addItem("Sem Cliente", None)
        for cliente in clientes:
            self.dialog.comboBox_clientes.addItem(cliente.nome, cliente.id_cliente)

    def obter_cliente_selecionado(self) -> int | None:
        """
        Retorna o ID do cliente selecionado no combobox,
        ou None se a opção 'Sem Cliente' estiver selecionada.
        """
        idx = self.dialog.comboBox_clientes.currentIndex()
        if idx == -1:
            return None
        return self.dialog.comboBox_clientes.itemData(idx)

    def adicionar_item(self):
        """
        Adiciona um item ao carrinho local e atualiza o estoque visual.
        """
        index = self.dialog.table_produtos.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self.dialog, "Aviso", "Selecione um produto")
            return
        produto = self.modelo_produtos._data[index.row()]
        if produto.quantidade_estoque <= 0:
            QMessageBox.warning(self.dialog, "Aviso", "Produto sem estoque disponível")
            return

        qtd_atual = self.carrinho_local.get(produto.id_produto, 0)
        self.carrinho_local[produto.id_produto] = qtd_atual + 1

        # Atualiza estoque visual (-1), só na UI, não no banco
        self.modelo_produtos.atualizar_quantidade_produto(produto.id_produto, -1)

        self.atualizar_carrinho_local()

    def remover_item(self):
        """
        Remove um item do carrinho local e atualiza o estoque visual.
        """
        index = self.dialog.table_carrinho.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self.dialog, "Aviso", "Selecione um item do carrinho")
            return
        item = self.modelo_carrinho._data[index.row()]
        id_produto = item.id_produto
        qtd_atual = self.carrinho_local.get(id_produto, 0)
        if qtd_atual <= 1:
            self.carrinho_local.pop(id_produto, None)
        else:
            self.carrinho_local[id_produto] = qtd_atual - 1

        # Atualiza estoque visual (+1), só na UI, não no banco
        self.modelo_produtos.atualizar_quantidade_produto(id_produto, +1)

        self.atualizar_carrinho_local()

    def atualizar_carrinho_local(self):
        """
        Atualiza os itens exibidos no carrinho, aplicando desconto de 5% caso
        cliente selecionado seja diferente de 'Sem Cliente'.
        """
        cliente_id = self.obter_cliente_selecionado()
        aplicar_desconto = cliente_id is not None  # Desconto se cliente selecionado

        itens_exibicao = []
        for id_produto, quantidade in self.carrinho_local.items():
            produto = next((p for p in self.modelo_produtos._data if p.id_produto == id_produto), None)
            if not produto:
                continue

            item_exibicao = type("ItemExibicao", (), {})()
            item_exibicao.id_produto = id_produto
            item_exibicao.quantidade = quantidade
            item_exibicao.preco_unitario = produto.preco

            # Aplica desconto se cliente válido
            if aplicar_desconto:
                item_exibicao.desconto_aplicado = (produto.preco * self.DESCONTO_CLIENTE).quantize(Decimal("0.01"))
            else:
                item_exibicao.desconto_aplicado = Decimal("0.00")

            itens_exibicao.append(item_exibicao)

        self.modelo_carrinho.atualizar_dados(itens_exibicao)
        self.atualizar_valor_total_local()

    def atualizar_valor_total_local(self):
        """
        Atualiza o valor total exibido na tela, considerando o desconto
        de 5% para clientes cadastrados.
        """
        cliente_id = self.obter_cliente_selecionado()
        aplicar_desconto = cliente_id is not None

        total = Decimal("0.0")
        for id_produto, quantidade in self.carrinho_local.items():
            produto = next((p for p in self.modelo_produtos._data if p.id_produto == id_produto), None)
            if produto:
                subtotal = produto.preco * quantidade
                if aplicar_desconto:
                    desconto = subtotal * self.DESCONTO_CLIENTE
                    subtotal -= desconto
                total += subtotal

        self.dialog.label_valorTotal.setText(f"Valor Total: R$ {total:.2f}")

    def concluir_compra(self):
        """
        Finaliza a compra reduzindo o estoque no banco e atualizando a UI.
        Aplica desconto visual na exibição, mas o banco registra o valor total
        sem desconto (pode ser adaptado para salvar desconto se desejar).
        """
        if not self.carrinho_local:
            QMessageBox.information(self.dialog, "Atenção", "Carrinho vazio")
            return

        try:
            # Reposição visual do estoque na UI antes da redução no banco
            for id_produto, quantidade in self.carrinho_local.items():
                self.modelo_produtos.atualizar_quantidade_produto(id_produto, quantidade)

            # Redução do estoque efetiva no banco
            for id_produto, quantidade in self.carrinho_local.items():
                self.produto_servico.reduzir_estoque(id_produto, quantidade)

            QMessageBox.information(self.dialog, "Sucesso", "Compra concluída com sucesso!")

            # Atualiza a tabela de produtos para refletir estoque atualizado
            self.carregar_produtos()

            # Limpa carrinho e atualiza UI
            self.carrinho_local.clear()
            self.atualizar_carrinho_local()

        except Exception as e:
            QMessageBox.critical(self.dialog, "Erro", f"Erro ao concluir compra: {str(e)}")

    def deslogar(self):
        """
        Fecha a janela atual e retorna ao sistema.
        """
        self.dialog.reject()
