# type: ignore[misc]

from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt, QAbstractTableModel
from typing import List
from src.modelos.tabelas_bd import Funcionario, Produto, Cliente
from src.servicos.servico_funcionario import FuncionarioServico
from src.servicos.servico_produto import ProdutoServico
from src.servicos.servico_cliente import ClienteServico


class SimpleTableModel(QAbstractTableModel):
    """
    Modelo para exibição do crud em uma lista simples.
    Recebe dados, nomes das colunas e função para mapear objetos em linhas.
    """

    def __init__(self, data: List, columns: List[str], row_to_values_func):
        super().__init__()
        self._data = data                      # Lista de objetos a exibir
        self._columns = columns                # Lista dos nomes das colunas
        self._row_to_values = row_to_values_func  # Função que extrai valores da linha

    def rowCount(self, parent=None) -> int:
        """Quantidade de linhas da tabela, igual ao número de objetos."""
        return len(self._data)

    def columnCount(self, parent=None) -> int:
        """Quantidade de colunas, baseada no tamanho da lista de colunas."""
        return len(self._columns)

    def data(self, index, role):
        """
        Retorna o dado para o índice dado, apenas para exibição.
        Ignora outras funções como edição, tooltip etc.
        """
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        row_obj = self._data[index.row()]
        # Retorna o valor da célula segundo a função de mapeamento
        return self._row_to_values(row_obj)[index.column()]

    def headerData(self, section, orientation, role):
        """
        Cabeçalhos horizontais da tabela (nomes das colunas).
        """
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._columns[section]

class controlador_telagerente:

    """
    Controlador principal da tela administrativa, conecta UI e serviços.
    Responsável pelo carregamento, busca, adição, edição e exclusão.
    """

    def __init__(self, funcionario_logado: Funcionario):
        # Funcionário que está logado no sistema
        self.funcionario_logado = funcionario_logado

        # Instância da camada de serviço para interação com dados
        self.funcionario_servico = FuncionarioServico()
        self.produto_servico = ProdutoServico()
        self.cliente_servico = ClienteServico()

        # Carrega a interface da UI via arquivo .ui do Qt Designer
        self.dialog: QDialog = uic.loadUi("src/interfaces/telas/Tela_Admin.ui")
        self.dialog.setWindowTitle(f"Painel Admin - {funcionario_logado.nome}")

        # Configura conexões dos eventos dos widgets da interface
        self.conectar_eventos()

        # Atualiza os CRUDS exibidos ao abrir a tela
        self.atualizar_listas()

    def conectar_eventos(self):
        """Vincula sinais dos botões e campos de texto às funções correspondentes."""
        # Botão para sair / deslogar
        self.dialog.botao_deslogar.clicked.connect(self.deslogar)

        # Eventos para CRUD funcionários e busca
        self.dialog.botao_adicionarFuncionario.clicked.connect(self.adicionar_usuario)
        self.dialog.botao_editarFuncionario.clicked.connect(self.editar_usuario)
        self.dialog.botao_excluirFuncionario.clicked.connect(self.excluir_usuario)
        self.dialog.lineEdit_buscaFuncionarios.textChanged.connect(self.buscar_funcionarios)

        # Eventos para CRUD produtos e busca
        self.dialog.botao_adicionarProduto.clicked.connect(self.adicionar_produto)
        self.dialog.botao_editarProduto.clicked.connect(self.editar_produto)
        self.dialog.botao_excluirProduto.clicked.connect(self.excluir_produto)
        self.dialog.lineEdit_buscaProdutos.textChanged.connect(self.buscar_produtos)

        # Eventos para CRUD clientes e busca
        self.dialog.botao_adicionarCliente.clicked.connect(self.adicionar_cliente)
        self.dialog.botao_editarCliente.clicked.connect(self.editar_cliente)
        self.dialog.botao_excluirCliente.clicked.connect(self.excluir_cliente)
        self.dialog.lineEdit_buscaClientes.textChanged.connect(self.buscar_clientes)

    def atualizar_listas(self):
        """Atualiza todas as tabelas da interface com dados atuais."""
        self.atualizar_lista_funcionarios()
        self.atualizar_lista_produtos()
        self.atualizar_lista_clientes()

    def atualizar_lista_funcionarios(self):
        """Carrega e exibe todos os funcionários na tabela correspondente."""
        funcionarios = self.funcionario_servico.buscar_todos_funcionarios()
        self.modelo_func = SimpleTableModel(
            funcionarios,
            ["ID", "Nome", "Usuário", "Cargo"],
            lambda f: [f.id_funcionario, f.nome, f.nome_usuario, f.cargo.value],
        )
        self.dialog.tableView_funcionarios.setModel(self.modelo_func)

    def atualizar_lista_produtos(self):
        """Carrega e exibe todos os produtos na tabela correspondente."""
        produtos = self.produto_servico.buscar_todos_produtos()
        self.modelo_prod = SimpleTableModel(
            produtos,
            ["ID", "Nome", "Preço", "Estoque"],
            lambda p: [p.id_produto, p.nome, f"R$ {p.preco:.2f}", p.quantidade_estoque],
        )
        self.dialog.tableView_produtos.setModel(self.modelo_prod)

    def atualizar_lista_clientes(self):
        """Carrega e exibe todos os clientes na tabela correspondente."""
        clientes = self.cliente_servico.buscar_todos_clientes()
        self.modelo_cliente = SimpleTableModel(
            clientes,
            ["ID", "Nome", "CPF", "Telefone"],
            lambda c: [c.id_cliente, c.nome, c.cpf, c.telefone],
        )
        self.dialog.tableView_clientes.setModel(self.modelo_cliente)

    def buscar_funcionarios(self):
        """
        Busca funcionário(s) por ID digitado na caixa de texto,
        ou exibe todos se o campo estiver vazio.
        """
        termo = self.dialog.lineEdit_buscaFuncionarios.text().strip()

        if termo == '':
            funcionarios = self.funcionario_servico.buscar_todos_funcionarios()
        elif termo.isdigit():
            funcionario = self.funcionario_servico.buscar_funcionario_por_id(int(termo))
            funcionarios = [funcionario] if funcionario else []
        else:
            funcionarios = []

        self.dialog.tableView_funcionarios.setModel(
            SimpleTableModel(
                funcionarios,
                ["ID", "Nome", "Usuário", "Cargo"],
                lambda f: [f.id_funcionario, f.nome, f.nome_usuario, f.cargo.value],
            )
        )

    def buscar_produtos(self):
        """
        Busca produto(s) por ID digitado na caixa de texto,
        ou exibe todos se o campo estiver vazio.
        """
        termo = self.dialog.lineEdit_buscaProdutos.text().strip()

        if termo == '':
            produtos = self.produto_servico.buscar_todos_produtos()
        elif termo.isdigit():
            produto = self.produto_servico.buscar_produto_por_id(int(termo))
            produtos = [produto] if produto else []
        else:
            produtos = []

        self.dialog.tableView_produtos.setModel(
            SimpleTableModel(
                produtos,
                ["ID", "Nome", "Preço", "Estoque"],
                lambda p: [p.id_produto, p.nome, f"R$ {p.preco:.2f}", p.quantidade_estoque],
            )
        )

    def buscar_clientes(self):
        """
        Busca cliente(s) por ID digitado na caixa de texto,
        ou exibe todos se o campo estiver vazio.
        """
        termo = self.dialog.lineEdit_buscaClientes.text().strip()

        if termo == '':
            clientes = self.cliente_servico.buscar_todos_clientes()
        elif termo.isdigit():
            cliente = self.cliente_servico.buscar_cliente_por_id(int(termo))
            clientes = [cliente] if cliente else []
        else:
            clientes = []

        self.dialog.tableView_clientes.setModel(
            SimpleTableModel(
                clientes,
                ["ID", "Nome", "CPF", "Telefone"],
                lambda c: [c.id_cliente, c.nome, c.cpf, c.telefone],
            )
        )

    def adicionar_usuario(self):
            form = uic.loadUi("src/interfaces/telas/Form_Usuario.ui")
            form.setWindowTitle("Cadastrar Funcionário")

            form.botao_enviarDados.clicked.connect(lambda: self._salvar_usuario(form))
            form.exec()

    def editar_usuario(self):
        sel = self.dialog.tableView_funcionarios.selectionModel().selectedRows()
        if not sel:
            QMessageBox.warning(self.dialog, "Atenção", "Selecione um funcionário para editar.")
            return

        func = self.modelo_func._data[sel[0].row()]
        form = uic.loadUi("src/interfaces/telas/Form_Usuario.ui")
        form.setWindowTitle(f"Editar Funcionário - {func.nome}")

        form.lineEdit_nome.setText(func.nome)
        form.lineEdit_nomeUsuario.setText(func.nome_usuario)
        form.comboBox_Cargo.setCurrentText(func.cargo.value)  # Ajustar se necessário para match exato

        # Senha vazia = não alterar
        form.lineEdit_senha.setText("")

        form.botao_enviarDados.clicked.connect(lambda: self._atualizar_usuario(form, func.id_funcionario))
        form.exec()

    def _salvar_usuario(self, form):
        try:
            nome = form.lineEdit_nome.text().strip()
            nome_usuario = form.lineEdit_nomeUsuario.text().strip()
            senha = form.lineEdit_senha.text()
            cargo_str = form.comboBox_Cargo.currentText()
            cargo = CargoEnum(cargo_str)  # Converte string para enum

            self.funcionario_servico.criar_funcionario(nome, cargo, nome_usuario, senha)
            QMessageBox.information(form, "Sucesso", "Funcionário cadastrado com sucesso.")
            form.close()
            self.atualizar_lista_funcionarios()
        except Exception as e:
            QMessageBox.critical(form, "Erro", str(e))

    def _atualizar_usuario(self, form, id_funcionario):
        try:
            nome = form.lineEdit_nome.text().strip()
            senha = form.lineEdit_senha.text()
            cargo_str = form.comboBox_Cargo.currentText()
            cargo = CargoEnum(cargo_str)

            senha_param = senha if senha else None

            self.funcionario_servico.atualizar_funcionario(id_funcionario, nome=nome, cargo=cargo, senha=senha_param)
            QMessageBox.information(form, "Sucesso", "Funcionário atualizado com sucesso.")
            form.close()
            self.atualizar_lista_funcionarios()
        except Exception as e:
            QMessageBox.critical(form, "Erro", str(e))

    def excluir_usuario(self):
        """Exclui funcionário selecionado da tabela, com confirmação e tratamento de erros."""
        selecao = self.dialog.tableView_funcionarios.selectionModel().selectedRows()
        if not selecao:
            QMessageBox.warning(self.dialog, "Atenção", "Selecione um funcionário para excluir.")
            return
        linha = selecao[0].row()
        id_funcionario = self.modelo_func._data[linha].id_funcionario
        try:
            self.funcionario_servico.deletar_funcionario(id_funcionario)
            self.atualizar_lista_funcionarios()
            QMessageBox.information(self.dialog, "Sucesso", "Funcionário excluído com sucesso.")
        except Exception as e:
            QMessageBox.critical(self.dialog, "Erro", f"Erro ao excluir: {e}")

    def adicionar_produto(self):
        form = uic.loadUi("src/interfaces/telas/Form_Produto.ui")
        form.setWindowTitle("Cadastrar Produto")

        form.botao_enviarDados.clicked.connect(lambda: self._salvar_produto(form))
        form.exec()

    def editar_produto(self):
        sel = self.dialog.tableView_produtos.selectionModel().selectedRows()
        if not sel:
            QMessageBox.warning(self.dialog, "Atenção", "Selecione um produto para editar.")
            return

        prod = self.modelo_prod._data[sel[0].row()]
        form = uic.loadUi("src/interfaces/telas/Form_Produto.ui")
        form.setWindowTitle(f"Editar Produto - {prod.nome}")

        form.lineEdit_nome.setText(prod.nome)
        form.lineEdit_descricao.setText(prod.descricao)
        form.lineEdit_quantidadeEstoque.setText(str(prod.quantidade_estoque))
        form.lineEdit_preco.setText(f"{prod.preco:.2f}")

        form.botao_enviarDados.clicked.connect(lambda: self._atualizar_produto(form, prod.id_produto))
        form.exec()

    def _salvar_produto(self, form):
        try:
            nome = form.lineEdit_nome.text().strip()
            descricao = form.lineEdit_descricao.text().strip()
            quantidade = int(form.lineEdit_quantidadeEstoque.text())
            preco = float(form.lineEdit_preco.text())

            self.produto_servico.criar_produto(nome, descricao, quantidade, preco)
            QMessageBox.information(form, "Sucesso", "Produto cadastrado com sucesso.")
            form.close()
            self.atualizar_lista_produtos()
        except Exception as e:
            QMessageBox.critical(form, "Erro", str(e))

    def _atualizar_produto(self, form, id_produto):
        try:
            nome = form.lineEdit_nome.text().strip()
            descricao = form.lineEdit_descricao.text().strip()
            quantidade = int(form.lineEdit_quantidadeEstoque.text())
            preco = float(form.lineEdit_preco.text())

            self.produto_servico.atualizar_produto(id_produto, nome, descricao, quantidade, preco)
            QMessageBox.information(form, "Sucesso", "Produto atualizado com sucesso.")
            form.close()
            self.atualizar_lista_produtos()
        except Exception as e:
            QMessageBox.critical(form, "Erro", str(e))

    def excluir_produto(self):
        """Exclui produto selecionado da tabela, com confirmação e tratamento de erros."""
        selecao = self.dialog.tableView_produtos.selectionModel().selectedRows()
        if not selecao:
            QMessageBox.warning(self.dialog, "Atenção", "Selecione um produto para excluir.")
            return
        linha = selecao[0].row()
        id_produto = self.modelo_prod._data[linha].id_produto
        try:
            self.produto_servico.deletar_produto(id_produto)
            self.atualizar_lista_produtos()
            QMessageBox.information(self.dialog, "Sucesso", "Produto excluído com sucesso.")
        except Exception as e:
            QMessageBox.critical(self.dialog, "Erro", f"Erro ao excluir: {e}")

    def adicionar_cliente(self):
        form = uic.loadUi("src/interfaces/telas/Form_Cliente.ui")
        form.setWindowTitle("Cadastrar Cliente")

        form.botao_enviarDados.clicked.connect(lambda: self._salvar_cliente(form))
        form.exec()

    def editar_cliente(self):
        sel = self.dialog.tableView_clientes.selectionModel().selectedRows()
        if not sel:
            QMessageBox.warning(self.dialog, "Atenção", "Selecione um cliente para editar.")
            return

        cli = self.modelo_cliente._data[sel[0].row()]
        form = uic.loadUi("src/interfaces/telas/Form_Cliente.ui")
        form.setWindowTitle(f"Editar Cliente - {cli.nome}")

        form.lineEdit_nome.setText(cli.nome)
        form.lineEdit_cpf.setText(cli.cpf)
        form.lineEdit_telefone.setText(cli.telefone)

        form.botao_enviarDados.clicked.connect(lambda: self._atualizar_cliente(form, cli.id_cliente))
        form.exec()

    def _salvar_cliente(self, form):
        try:
            nome = form.lineEdit_nome.text().strip()
            cpf = form.lineEdit_cpf.text().strip()
            telefone = form.lineEdit_telefone.text().strip()

            self.cliente_servico.criar_cliente(nome, cpf, telefone)
            QMessageBox.information(form, "Sucesso", "Cliente cadastrado com sucesso.")
            form.close()
            self.atualizar_lista_clientes()
        except Exception as e:
            QMessageBox.critical(form, "Erro", str(e))

    def _atualizar_cliente(self, form, id_cliente):
        try:
            nome = form.lineEdit_nome.text().strip()
            telefone = form.lineEdit_telefone.text().strip()

            self.cliente_servico.atualizar_cliente(id_cliente, nome, telefone)
            QMessageBox.information(form, "Sucesso", "Cliente atualizado com sucesso.")
            form.close()
            self.atualizar_lista_clientes()
        except Exception as e:
            QMessageBox.critical(form, "Erro", str(e))

    def excluir_cliente(self):
        """Exclui cliente selecionado da tabela, com confirmação e tratamento de erros."""
        selecao = self.dialog.tableView_clientes.selectionModel().selectedRows()
        if not selecao:
            QMessageBox.warning(self.dialog, "Atenção", "Selecione um cliente para excluir.")
            return
        linha = selecao[0].row()
        id_cliente = self.modelo_cliente._data[linha].id_cliente
        try:
            self.cliente_servico.deletar_cliente(id_cliente)
            self.atualizar_lista_clientes()
            QMessageBox.information(self.dialog, "Sucesso", "Cliente excluído com sucesso.")
        except Exception as e:
            QMessageBox.critical(self.dialog, "Erro", f"Erro ao excluir: {e}")

    def deslogar(self):
        """Fecha a janela da aplicação (logout)."""
        self.dialog.close()

    def executar(self):
        """Executa a tela."""
        self.dialog.exec()
