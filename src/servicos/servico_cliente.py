import re
from typing import Optional, List
from src.modelos.tabelas_bd import Cliente
from src.repositorios.repositorio_cliente import ClienteRepositorio

"""
Este arquivo implementa o serviço para operações de negócio da entidade Cliente,
seguindo o padrão Service Layer. Encapsula todas as regras de negócio relacionadas
ao cadastro e gerenciamento de clientes, incluindo validação de CPF e controle
de duplicatas, fornecendo uma camada de abstração entre a lógica de negócio
e o acesso aos dados da aplicação.
"""


class ClienteServico:
    """Serviço para regras de negócio da entidade Cliente."""

    def __init__(self):
        self.cliente_repo = ClienteRepositorio()

    def criar_cliente(self, nome: str, cpf: str, telefone: str = None) -> Cliente:
        """RF02 - Cadastro de Clientes"""
        # Validação de dados (RN04)
        if not nome or nome.strip() == "":
            raise Exception("Nome do cliente não pode ser vazio")

        if not self.validar_cpf(cpf):
            raise Exception("CPF inválido")

        if self.verificar_cpf_existente(cpf):
            raise Exception("CPF já cadastrado no sistema")

        cliente = Cliente(
            nome=nome.strip(),
            cpf=cpf,
            telefone=telefone.strip() if telefone else None
        )

        return self.cliente_repo.salvar(cliente)

    def buscar_cliente_por_id(self, id_cliente: int) -> Optional[Cliente]:
        if id_cliente <= 0:
            raise Exception(
                "ID do cliente deve ser maior que zero")

        return self.cliente_repo.buscar_por_id(id_cliente)

    def buscar_todos_clientes(self) -> List[Cliente]:
        return self.cliente_repo.buscar_todos()

    def buscar_cliente_por_cpf(self, cpf: str) -> Optional[Cliente]:
        if not self.validar_cpf(cpf):
            raise Exception("CPF inválido")

        return self.cliente_repo.buscar_por_cpf(cpf)

    def buscar_clientes_por_nome(self, nome: str) -> List[Cliente]:
        if not nome or nome.strip() == "":
            return []

        return self.cliente_repo.buscar_por_nome(nome.strip())

    def atualizar_cliente(self, id_cliente: int, nome: str = None,
                          telefone: str = None) -> Cliente:
        cliente = self.cliente_repo.buscar_por_id(id_cliente)
        if not cliente:
            raise Exception(
                f"Cliente com ID {id_cliente} não encontrado")

        if nome is not None:
            if not nome or nome.strip() == "":
                raise Exception(
                    "Nome do cliente não pode ser vazio")
            cliente.nome = nome.strip()

        if telefone is not None:
            cliente.telefone = telefone.strip() if telefone else None

        return self.cliente_repo.atualizar(cliente)

    def deletar_cliente(self, id_cliente: int) -> bool:
        cliente = self.cliente_repo.buscar_por_id(id_cliente)
        if not cliente:
            raise Exception(
                f"Cliente com ID {id_cliente} não encontrado")

        return self.cliente_repo.deletar(id_cliente)

    def validar_cpf(self, cpf: str) -> bool:
        """RN04 - Validação de CPF"""
        if not cpf:
            return False

        # Remove caracteres não numéricos
        cpf = re.sub(r'[^0-9]', '', cpf)

        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False

        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False

        # Calcula primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        # Calcula segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        return cpf[9] == str(digito1) and cpf[10] == str(digito2)

    def verificar_cpf_existente(self, cpf: str) -> bool:
        """RN04 - CPF deve ser único no sistema"""
        cliente_existente = self.cliente_repo.buscar_por_cpf(cpf)
        return cliente_existente is not None
