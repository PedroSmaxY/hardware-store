from typing import Optional
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from src.modelos.tabelas_bd import Funcionario, CargoEnum

"""
Controlador responsável por gerenciar a tela de login do sistema,
incluindo autenticação de funcionários e controle de acesso.
"""


class ControladorLogin:
    """Controlador para a tela de login."""

    def __init__(self):
        # Carregar a interface do arquivo .ui
        self.dialog = uic.loadUi(
            "src/interfaces/telas/Tela_Login.ui")
        self.funcionario_logado: Optional[Funcionario] = None

        # Configurar interface
        self.configurar_interface()
        self.conectar_eventos()

    def configurar_interface(self):
        """Configurações iniciais da interface de login."""
        # Definir título da janela
        self.dialog.setWindowTitle("Sistema de Loja de Ferragens - Login")

        # Focar no campo de usuário
        self.dialog.lineEdit.setFocus()

        # Placeholder nos campos
        self.dialog.lineEdit.setPlaceholderText("Digite seu usuário")
        self.dialog.lineEdit_2.setPlaceholderText("Digite sua senha")

    def conectar_eventos(self):
        """Conecta eventos da interface de login."""
        # Botão entrar
        self.dialog.pushButton.clicked.connect(self.fazer_login)

        # Enter nos campos para fazer login
        self.dialog.lineEdit.returnPressed.connect(self.fazer_login)
        self.dialog.lineEdit_2.returnPressed.connect(self.fazer_login)

    def fazer_login(self):
        """Realiza o processo de autenticação."""
        usuario = self.dialog.lineEdit.text().strip()
        senha = self.dialog.lineEdit_2.text()

        # Validar campos
        if not usuario:
            self.mostrar_erro("Por favor, digite o usuário!")
            self.dialog.lineEdit.setFocus()
            return

        if not senha:
            self.mostrar_erro("Por favor, digite a senha!")
            self.dialog.lineEdit_2.setFocus()
            return

        try:
            # MOCK - Simular autenticação (remover quando serviço estiver pronto)
            funcionario = self.autenticar_mock(usuario, senha)

            if funcionario:
                self.funcionario_logado = funcionario
                self.mostrar_sucesso(f"Bem-vindo(a), {funcionario.nome}!")
                self.dialog.accept()  # Fecha o dialog com sucesso
            else:
                self.mostrar_erro("Usuário ou senha incorretos!")
                self.limpar_campos()
                self.dialog.lineEdit.setFocus()

        except Exception as e:
            self.mostrar_erro(f"Erro ao fazer login: {str(e)}")
            self.limpar_campos()

    def autenticar_mock(self, usuario: str, senha: str) -> Optional[Funcionario]:
        """MOCK - Simula autenticação de funcionário."""
        # Usuários de teste
        usuarios_teste = {
            "admin": {"senha": "123456", "nome": "Administrador", "cargo": CargoEnum.GERENTE},
            "vendedor": {"senha": "123", "nome": "João Vendedor", "cargo": CargoEnum.VENDEDOR},
            "estoquista": {"senha": "456", "nome": "Maria Estoque", "cargo": CargoEnum.ESTOQUISTA}
        }

        if usuario in usuarios_teste and usuarios_teste[usuario]["senha"] == senha:
            # Criar funcionário mock
            dados = usuarios_teste[usuario]
            funcionario = Funcionario(
                nome=dados["nome"],
                nome_usuario=usuario,
                senha=senha,
                cargo=dados["cargo"],
                salario=3000.0
            )
            # Simular ID do banco
            funcionario.id = 1
            return funcionario

        return None

    def limpar_campos(self):
        """Limpa os campos de usuário e senha."""
        self.dialog.lineEdit.clear()
        self.dialog.lineEdit_2.clear()

    def mostrar_erro(self, mensagem: str):
        """Exibe mensagem de erro."""
        QMessageBox.critical(self.dialog, "Erro", mensagem)

    def mostrar_sucesso(self, mensagem: str):
        """Exibe mensagem de sucesso."""
        QMessageBox.information(self.dialog, "Sucesso", mensagem)

    def executar(self) -> bool:
        """Executa o dialog de login e retorna True se login bem-sucedido."""
        resultado = self.dialog.exec()
        return resultado == QDialog.DialogCode.Accepted

    def get_funcionario_logado(self) -> Optional[Funcionario]:
        """Retorna o funcionário que fez login."""
        return self.funcionario_logado
