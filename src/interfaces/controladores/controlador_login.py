# type: ignore[misc]

from typing import Optional
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from src.modelos.tabelas_bd import Funcionario
from src.servicos.servico_funcionario import FuncionarioServico

"""
Controlador responsável por gerenciar a tela de login do sistema,
incluindo autenticação de funcionários e controle de acesso.
"""

class ControladorLogin:
    """Controlador para a tela de login."""

    def __init__(self):
        self.funcionario_servico = FuncionarioServico()
        self.funcionario_logado: Optional[Funcionario] = None

        # Carrega a interface
        self.dialog = uic.loadUi("src/interfaces/telas/Tela_Login.ui")
        self.configurar_interface()
        self.conectar_eventos()

    def configurar_interface(self):
        """Configurações iniciais da interface de login."""
        self.dialog.setWindowTitle("Sistema de Loja de Hardware - Login")
        self.dialog.lineEdit.setFocus()
        self.dialog.lineEdit.setPlaceholderText("Digite seu usuário")
        self.dialog.lineEdit_2.setPlaceholderText("Digite sua senha")

    def conectar_eventos(self):
        """Conecta eventos da interface de login."""
        self.dialog.pushButton.clicked.connect(self.fazer_login)
        self.dialog.lineEdit.returnPressed.connect(self.fazer_login)
        self.dialog.lineEdit_2.returnPressed.connect(self.fazer_login)

    def fazer_login(self):
        """Realiza o processo de autenticação."""
        usuario = self.dialog.lineEdit.text().strip()
        senha = self.dialog.lineEdit_2.text()

        if not usuario:
            self.mostrar_erro("Por favor, digite o usuário!")
            self.dialog.lineEdit.setFocus()
            return

        if not senha:
            self.mostrar_erro("Por favor, digite a senha!")
            self.dialog.lineEdit_2.setFocus()
            return

        try:
            funcionario = self.funcionario_servico.autenticar_funcionario(usuario, senha)

            if funcionario:
                self.funcionario_logado = funcionario
                self.mostrar_sucesso(f"Bem-vindo(a), {funcionario.nome}!")
                self.dialog.accept()
            else:
                self.mostrar_erro("Usuário ou senha incorretos!")
                self.limpar_campos()
                self.dialog.lineEdit.setFocus()

        except Exception as e:
            self.mostrar_erro(f"Erro ao fazer login: {str(e)}")
            self.limpar_campos()

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
