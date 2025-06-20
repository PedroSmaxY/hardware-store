# type: ignore[misc]

from typing import List
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt, QAbstractTableModel

from src.modelos.tabelas_bd import Funcionario, Produto, Cliente, CargoEnum
from src.servicos.servico_funcionario import FuncionarioServico
from src.servicos.servico_produto import ProdutoServico
from src.servicos.servico_cliente import ClienteServico

class SimpleTableModel(QAbstractTableModel):
    """
    Modelo de tabela simples para uso com QTableView, 
    parametrizado para qualquer lista de objetos com colunas dinâmicas.
    """

    def __init__(self, data: List, columns: List[str], row_to_values_func):

        super().__init__()
        self._data = data
        self._columns = columns
        self._row_to_values = row_to_values_func

    """Construção do modelo do CRUD / Tabela."""
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


class ControladorTelaGerente:
    """
    Controlador principal da interface administrativa para gerenciar funcionários,
    produtos e clientes, com operações CRUD integradas aos serviços.
    """

    def __init__(self, funcionario_logado: Funcionario):
        """
        Inicializa a tela e serviços, além de carregar a interface gráfica e os dados iniciais.
        Define o título da janela com o nome do usuário logado.
        """
        self.funcionario_logado = funcionario_logado

        # Instância os serviços que lidam com a lógica de negócio
        self.funcionario_servico = FuncionarioServico()
        self.produto_servico = ProdutoServico()
        self.cliente_servico = ClienteServico()

        # Carrega a interface Qt Designer e define título com nome do funcionário logado
        self.dialog: QDialog = uic.loadUi("src/interfaces/telas/Tela_Admin.ui")
        self.dialog.setWindowTitle(f"Painel Admin - {funcionario_logado.nome}")

        self.conectar_eventos()
        self.atualizar_listas()

    def conectar_eventos(self):
        """
        Conecta os sinais dos botões e campos de busca aos métodos correspondentes,
        permitindo interação do usuário.
        """
        # Botão de logout
        self.dialog.botao_deslogar.clicked.connect(self.deslogar)

        # Eventos relacionados a funcionários
        self.dialog.botao_adicionarFuncionario.clicked.connect(self.adicionar_funcionario)
        self.dialog.botao_editarFuncionario.clicked.connect(self.editar_funcionario)
        self.dialog.botao_excluirFuncionario.clicked.connect(self.excluir_funcionario)
        self.dialog.lineEdit_buscaFuncionarios.textChanged.connect(self.buscar_funcionarios)

        # Eventos relacionados a produtos
        self.dialog.botao_adicionarProduto.clicked.connect(self.adicionar_produto)
        self.dialog.botao_editarProduto.clicked.connect(self.editar_produto)
        self.dialog.botao_excluirProduto.clicked.connect(self.excluir_produto)
        self.dialog.lineEdit_buscaProdutos.textChanged.connect(self.buscar_produtos)

        # Eventos relacionados a clientes
        self.dialog.botao_adicionarCliente.clicked.connect(self.adicionar_cliente)
        self.dialog.botao_editarCliente.clicked.connect(self.editar_cliente)
        self.dialog.botao_excluirCliente.clicked.connect(self.excluir_cliente)
        self.dialog.lineEdit_buscaClientes.textChanged.connect(self.buscar_clientes)

    def atualizar_listas(self):
        """Atualiza todas as tabelas da interface com os dados atuais do banco."""
        self.atualizar_lista_funcionarios()
        self.atualizar_lista_produtos()
        self.atualizar_lista_clientes()

    def atualizar_lista_funcionarios(self):
        """Atualiza a tabela de funcionários com dados atuais."""
        funcionarios = self.funcionario_servico.buscar_todos_funcionarios()
        self.modelo_func = SimpleTableModel(
            funcionarios,
            ["ID", "Nome", "Usuário", "Cargo"],
            lambda f: [f.id_funcionario, f.nome, f.nome_usuario, f.cargo.value],
        )
        self.dialog.tableView_funcionarios.setModel(self.modelo_func)

    def atualizar_lista_produtos(self):
        """Atualiza a tabela de produtos com dados atuais."""
        produtos = self.produto_servico.buscar_todos_produtos()
        self.modelo_prod = SimpleTableModel(
            produtos,
            ["ID", "Nome", "Preço", "Estoque"],
            lambda p: [p.id_produto, p.nome, f"R$ {p.preco:.2f}", p.quantidade_estoque],
        )
        self.dialog.tableView_produtos.setModel(self.modelo_prod)

    def atualizar_lista_clientes(self):
        """Atualiza a tabela de clientes com dados atuais."""
        clientes = self.cliente_servico.buscar_todos_clientes()
        self.modelo_cliente = SimpleTableModel(
            clientes,
            ["ID", "Nome", "CPF", "Telefone"],
            lambda c: [c.id_cliente, c.nome, c.cpf, c.telefone],
        )
        self.dialog.tableView_clientes.setModel(self.modelo_cliente)

    def buscar_funcionarios(self):
        """
        Busca funcionário(s) por ID digitado no campo de busca.
        Se vazio, exibe todos os funcionários.
        O valor escrito, deve ser um número.
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
        Busca produto(s) por ID digitado no campo de busca.
        Se vazio, exibe todos os produtos.
        O valor escrito, deve ser um número.
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
        Busca cliente(s) por ID digitado no campo de busca.
        Se vazio, exibe todos os clientes.
        O valor escrito, deve ser um número.
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

    def adicionar_funcionario(self):
        """
        Abre o formulário para cadastro de novo funcionário e conecta o botão de envio
        à função que processa a criação.
        """

        form = uic.loadUi("src/interfaces/telas/Form_Funcionario.ui")
        form.setWindowTitle("Cadastrar Funcionário") # Define o título da tela.

        form.botao_enviarDados.clicked.connect(lambda: self._salvar_funcionario(form)) # Define a função executada pelo botão de enviar.
        form.exec()

    def editar_funcionario(self):
        """
        Abre o formulário de edição para o funcionário selecionado na tabela.
        Se nenhum for selecionado, exibe aviso.
        """
        sel = self.dialog.tableView_funcionarios.selectionModel().selectedRows()
        if not sel:
            QMessageBox.warning(self.dialog, "Atenção", "Selecione um funcionário para editar.")
            return

        func = self.modelo_func._data[sel[0].row()]
        form = uic.loadUi("src/interfaces/telas/Form_Funcionario.ui")
        form.setWindowTitle(f"Editar Funcionário - {func.nome}")

        # Preenche os campos com dados atuais do funcionário
        form.lineEdit_nome.setText(func.nome)
        form.lineEdit_nomeUsuario.setText(func.nome_usuario)
        form.comboBox_Cargo.setCurrentText(func.cargo.value)

        # Campo senha fica vazio para não alterar a menos que o usuário digite
        form.lineEdit_senha.setText("")

        form.botao_enviarDados.clicked.connect(lambda: self._atualizar_funcionario(form, func.id_funcionario))
        form.exec()

    def _salvar_funcionario(self, form):
        """
        Processa o cadastro de funcionário após submissão do formulário,
        capturando dados, chamando serviço e atualizando a lista.
        Exibe mensagem de erro caso ocorra exceção.
        """
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

    def _atualizar_funcionario(self, form, id_funcionario):
        """
        Processa a atualização do funcionário após submissão do formulário de edição,
        aceitando atualização condicional da senha e atualizando lista após sucesso.
        """
        try:
            nome = form.lineEdit_nome.text().strip()
            nome_usuario = form.lineEdit_nomeUsuario.text().strip() 
            senha = form.lineEdit_senha.text()
            cargo_str = form.comboBox_Cargo.currentText()
            cargo = CargoEnum(cargo_str)

            senha_param = senha if senha else None  # Se vazio, não altera a senha

            self.funcionario_servico.atualizar_funcionario(
                id_funcionario,
                nome=nome,
                cargo=cargo,
                nome_usuario=nome_usuario, 
                senha=senha_param
            )

            QMessageBox.information(form, "Sucesso", "Funcionário atualizado com sucesso.")
            form.close()
            self.atualizar_lista_funcionarios()
        except Exception as e:
            QMessageBox.critical(form, "Erro", str(e))

    def excluir_funcionario(self, id_funcionario: int) -> bool:
        """
        Deleta funcionário pelo ID.
        Lança exceção se não encontrar funcionário com o ID.
        Retorna o resultado da operação via serviço.
        """
        funcionario = self.funcionario_servico.buscar_funcionario_por_id(id_funcionario)
        if not funcionario:
            raise Exception(f"Funcionário com ID {id_funcionario} não encontrado")
        return self.funcionario_servico.deletar(id_funcionario)

    def adicionar_produto(self):
        """
        Abre o formulário para cadastro de novo produto,
        conectando o botão de envio à função de criação.
        """
        form = uic.loadUi("src/interfaces/telas/Form_Produto.ui")
        form.setWindowTitle("Cadastrar Produto")

        form.botao_enviarDados.clicked.connect(lambda: self._salvar_produto(form))
        form.exec()

    def editar_produto(self):
        """
        Abre formulário para editar produto selecionado.
        Exibe aviso se nenhum selecionado.
        Preenche os campos com dados atuais do produto.
        """
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
        """
        Processa o cadastro de produto após submissão do formulário,
        validando e enviando para o serviço, atualizando lista em caso de sucesso.
        """
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
        """
        Processa atualização de produto, semelhante ao cadastro,
        alterando dados conforme formulário e atualizando a lista.
        """
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

    def excluir_produto(self, id_produto: int) -> bool:
        """
        Deleta produto pelo ID, lança exceção se não encontrado,
        e retorna resultado da operação.
        """
        produto = self.produto_servico.buscar_produto_por_id(id_produto)
        if not produto:
            raise Exception(f"Produto com ID {id_produto} não encontrado")
        return self.produto_servico.deletar(id_produto)

    def adicionar_cliente(self):
        """
        Abre formulário para cadastro de cliente e conecta botão de envio.
        """
        form = uic.loadUi("src/interfaces/telas/Form_Cliente.ui")
        form.setWindowTitle("Cadastrar Cliente")

        form.botao_enviarDados.clicked.connect(lambda: self._salvar_cliente(form))
        form.exec()

    def editar_cliente(self):
        """
        Abre formulário para edição de cliente selecionado.
        Exibe aviso se nenhum selecionado.
        Preenche os campos com dados do cliente.
        """
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
        """
        Processa cadastro de cliente, valida dados e atualiza lista após sucesso.
        """
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
        """
        Processa atualização de cliente com dados alterados e atualiza lista.
        """
        try:
            nome = form.lineEdit_nome.text().strip()
            telefone = form.lineEdit_telefone.text().strip()

            self.cliente_servico.atualizar_cliente(id_cliente, nome, telefone)
            QMessageBox.information(form, "Sucesso", "Cliente atualizado com sucesso.")
            form.close()
            self.atualizar_lista_clientes()
        except Exception as e:
            QMessageBox.critical(form, "Erro", str(e))

    def excluir_cliente(self, id_cliente: int) -> bool:
        """
        Deleta cliente pelo ID, lança exceção se não encontrado,
        e retorna o resultado da exclusão.
        """
        cliente = self.cliente_servico.buscar_cliente_por_id(id_cliente)
        if not cliente:
            raise Exception(f"Cliente com ID {id_cliente} não encontrado")
        return self.cliente_servico.deletar(id_cliente)

    def deslogar(self):
        """Fecha a janela da aplicação, efetivando o logout do usuário."""
        self.dialog.close()

    def executar(self):
        """Executa o loop modal da janela principal da interface."""
        self.dialog.exec()
