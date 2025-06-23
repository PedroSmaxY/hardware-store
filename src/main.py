import sys
from PyQt6.QtWidgets import QApplication, QMessageBox  # type: ignore
from src.configs.config_bd import iniciar_bd
from src.interfaces.controladores.controlador_login import ControladorLogin
from src.interfaces.controladores.controlador_telagerente import ControladorTelaGerente

"""
Arquivo principal do sistema de loja de hardware.
Responsável por inicializar o banco de dados, gerenciar o login
e coordenar o fluxo principal da aplicação.
"""


def main():

    """Função principal do sistema."""
    print("🔧 Iniciando Sistema da Loja de Hardware...")

    # Inicializar banco de dados
    try:
        print("📊 Inicializando banco de dados...")
        iniciar_bd()
        print("✅ Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        return

    # Criar aplicação Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Sistema de Loja de Hardware")
    app.setOrganizationName("Hardware Store")

    try:
        print("🔐 Carregando tela de login...")

        # Criar e executar login
        controlador_login = ControladorLogin()

        if controlador_login.executar():
            funcionario = controlador_login.get_funcionario_logado()
            print(
                f"✅ Login realizado! Usuário: {funcionario.nome if funcionario else 'Desconhecido'}")

            cargo = funcionario.cargo

            if cargo.name == "GERENTE":
                controlador = ControladorTelaGerente(funcionario)
            # elif cargo.name == "VENDEDOR":
            #    controlador = ControladorTelaVendedor(funcionario)
            else:
                QMessageBox.critical(None, "Erro", f"Cargo não reconhecido: {cargo}")
                return

            controlador.executar() 

        else:
            print("🚫 Login cancelado pelo usuário.")
            QMessageBox.information(
                None, "Sistema", "Login cancelado. Encerrando sistema.")

    except Exception as e:
        error_msg = f"Erro ao inicializar sistema: {str(e)}"
        print(f"❌ {error_msg}")
        QMessageBox.critical(None, "Erro Crítico", error_msg)

    print("🔄 Encerrando aplicação...")
