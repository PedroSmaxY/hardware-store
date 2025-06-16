import sys
from PyQt6.QtWidgets import QApplication
from src.configs.config_bd import iniciar_bd

# TODO: Implementar o restante do código principal do sistema de loja de hardware


def main():
    iniciar_bd()

    app = QApplication(sys.argv)

    sys.exit(app.exec())
