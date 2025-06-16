import sys
from PyQt6.QtWidgets import QApplication, QMessageBox  # type: ignore
from src.configs.config_bd import iniciar_bd
from src.interfaces.controladores.controlador_login import ControladorLogin

"""
Arquivo principal do sistema de loja de hardware.
Responsável por inicializar o banco de dados, gerenciar o login
e coordenar o fluxo principal da aplicação.
"""


def main():
    """Função principal do sistema."""
    print("🔧 Iniciando Sistema de Loja de Ferragens...")

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
    app.setApplicationName("Sistema de Loja de Ferragens")
    app.setOrganizationName("Hardware Store")

    try:
        print("🔐 Carregando tela de login...")

        # Criar e executar login
        controlador_login = ControladorLogin()

        if controlador_login.executar():
            funcionario = controlador_login.get_funcionario_logado()
            print(
                f"✅ Login realizado! Usuário: {funcionario.nome if funcionario else 'Desconhecido'}")

            # TODO: Implementar tela principal do sistema
            QMessageBox.information(
                None,
                "Sistema Iniciado",
                f"Bem-vindo(a), {funcionario.nome if funcionario else 'Usuário'}!\n\n"
                f"Cargo: {funcionario.cargo.value if funcionario else 'N/A'}\n\n"
                "💡 Sistema funcionando!\n"
                "(Tela principal será implementada em breve)"
            )

            # Placeholder - manter aplicação rodando
            print("🚀 Sistema pronto para uso!")
            print("📝 Próximos passos: Implementar tela principal")

        else:
            print("🚫 Login cancelado pelo usuário.")
            QMessageBox.information(
                None, "Sistema", "Login cancelado. Encerrando sistema.")

    except Exception as e:
        error_msg = f"Erro ao inicializar sistema: {str(e)}"
        print(f"❌ {error_msg}")
        QMessageBox.critical(None, "Erro Crítico", error_msg)

    print("🔄 Encerrando aplicação...")
