import hashlib
from typing import List, Optional
from src.modelos.tabelas_bd import Funcionario, CargoEnum
from src.repositorios.repositorio_funcionario import FuncionarioRepositorio

"""
Este arquivo implementa o serviço para operações de negócio da entidade Funcionario,
seguindo o padrão Service Layer. Encapsula todas as regras de negócio relacionadas
ao gerenciamento de funcionários, autenticação e controle de acesso, incluindo
criptografia de senhas e validação de credenciais, fornecendo uma camada de
abstração entre a lógica de negócio e o acesso aos dados da aplicação.
"""


class FuncionarioServico:
    """Serviço para regras de negócio da entidade Funcionario."""

    def __init__(self):
        self.funcionario_repo = FuncionarioRepositorio()

    def criar_funcionario(self, nome: str, cargo: CargoEnum, nome_usuario: str, senha: str) -> Funcionario:
        """RF03 - Cadastro de Funcionários (apenas gerente pode cadastrar - RN01)"""
        # Validações
        if not nome or nome.strip() == "":
            raise Exception("Nome do funcionário não pode ser vazio")

        if not nome_usuario or nome_usuario.strip() == "":
            raise Exception("Nome de usuário não pode ser vazio")

        if len(senha) < 6:
            raise Exception("Senha deve ter pelo menos 6 caracteres")

        if self.verificar_nome_usuario_existente(nome_usuario):
            raise Exception("Nome de usuário já existe no sistema")

        funcionario = Funcionario(
            nome=nome.strip().capitalize(),
            cargo=cargo,
            nome_usuario=nome_usuario.strip(),
            senha=self.criptografar_senha(senha)
        )

        return self.funcionario_repo.salvar(funcionario)

    def buscar_funcionario_por_id(self, id_funcionario: int) -> Optional[Funcionario]:
        if id_funcionario <= 0:
            raise Exception("ID do funcionário deve ser maior que zero")

        return self.funcionario_repo.buscar_por_id(id_funcionario)

    def buscar_todos_funcionarios(self) -> List[Funcionario]:
        return self.funcionario_repo.buscar_todos()

    def buscar_funcionario_por_nome_usuario(self, nome_usuario: str) -> Optional[Funcionario]:
        if not nome_usuario or nome_usuario.strip() == "":
            return None

        return self.funcionario_repo.buscar_por_nome_usuario(nome_usuario.strip())

    def buscar_funcionarios_por_cargo(self, cargo: CargoEnum) -> List[Funcionario]:
        return self.funcionario_repo.buscar_por_cargo(cargo)

    def atualizar_funcionario(self, id_funcionario: int, nome: str = None,
                              cargo: CargoEnum = None, senha: str = None) -> Funcionario:
        """Apenas gerente pode alterar funcionários (RN01)"""
        funcionario = self.funcionario_repo.buscar_por_id(id_funcionario)
        if not funcionario:
            raise Exception(
                f"Funcionário com ID {id_funcionario} não encontrado")

        if nome is not None:
            if not nome or nome.strip() == "":
                raise Exception(
                    "Nome do funcionário não pode ser vazio")
            funcionario.nome = nome.strip()

        if cargo is not None:
            funcionario.cargo = cargo

        if senha is not None:
            if len(senha) < 6:
                raise Exception(
                    "Senha deve ter pelo menos 6 caracteres")
            funcionario.senha = self.criptografar_senha(senha)

        return self.funcionario_repo.atualizar(funcionario)

    def deletar_funcionario(self, id_funcionario: int) -> bool:
        """Apenas gerente pode deletar funcionários (RN01)"""
        funcionario = self.funcionario_repo.buscar_por_id(id_funcionario)
        if not funcionario:
            raise Exception(
                f"Funcionário com ID {id_funcionario} não encontrado")

        return self.funcionario_repo.deletar(id_funcionario)

    def autenticar_funcionario(self, nome_usuario: str, senha: str) -> Optional[Funcionario]:
        """RF01 - Sistema de Login"""
        if not nome_usuario or not senha:
            raise Exception(
                "Nome de usuário e senha são obrigatórios")

        funcionario = self.funcionario_repo.buscar_por_nome_usuario(
            nome_usuario.strip())
        if not funcionario:
            raise Exception("Credenciais inválidas")

        if not self.verificar_senha(senha, funcionario.senha):
            raise Exception("Credenciais inválidas")

        return funcionario

    def verificar_nome_usuario_existente(self, nome_usuario: str) -> bool:
        funcionario_existente = self.funcionario_repo.buscar_por_nome_usuario(
            nome_usuario)
        return funcionario_existente is not None

    def criptografar_senha(self, senha: str) -> str:
        """RNF02 - Segurança: senhas devem ser criptografadas"""
        return hashlib.sha256(senha.encode()).hexdigest()

    def verificar_senha(self, senha: str, senha_hash: str) -> bool:
        """Verifica se a senha corresponde ao hash armazenado"""
        return self.criptografar_senha(senha) == senha_hash
