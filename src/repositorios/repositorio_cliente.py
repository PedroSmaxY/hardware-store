from typing import List, Optional
from sqlalchemy.orm import Session
from src.configs.config_bd import Session as SessionLocal
from src.modelos.tabelas_bd import Cliente

"""
Este arquivo implementa o repositório para operações CRUD da entidade Cliente,
seguindo o padrão Repository. Encapsula todas as operações de acesso a dados
relacionadas aos clientes, fornecendo uma camada de abstração entre o modelo
de dados e a lógica de negócio da aplicação.
"""


class ClienteRepositorio:
    """Repositório para operações CRUD da entidade Cliente."""

    def __init__(self, session: Session | None = None):
        self.session = session or SessionLocal()

    def salvar(self, cliente: Cliente) -> Cliente:
        """Salva um cliente no banco de dados."""
        try:
            self.session.add(cliente)
            self.session.commit()
            self.session.refresh(cliente)
            return cliente
        except Exception as e:
            self.session.rollback()
            raise e

    def criar(self, nome: str, cpf: str, telefone: Optional[str] = None) -> Cliente:
        """Cria um novo cliente no banco de dados."""
        try:
            cliente = Cliente(
                nome=nome,
                cpf=cpf,
                telefone=telefone
            )
            self.session.add(cliente)
            self.session.commit()
            self.session.refresh(cliente)
            return cliente
        except Exception as e:
            self.session.rollback()
            raise e

    def buscar_por_id(self, id_cliente: int) -> Optional[Cliente]:
        """Busca um cliente pelo ID."""
        return self.session.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()

    def buscar_todos(self) -> List[Cliente]:
        """Retorna todos os clientes cadastrados."""
        return self.session.query(Cliente).all()

    def buscar_por_cpf(self, cpf: str) -> Optional[Cliente]:
        """Busca um cliente pelo CPF."""
        return self.session.query(Cliente).filter(Cliente.cpf == cpf).first()

    def buscar_por_nome(self, nome: str) -> List[Cliente]:
        """Busca clientes pelo nome (busca parcial)."""
        return self.session.query(Cliente).filter(
            Cliente.nome.ilike(f"%{nome}%")
        ).all()

    def buscar_por_telefone(self, telefone: str) -> Optional[Cliente]:
        """Busca um cliente pelo telefone."""
        return self.session.query(Cliente).filter(Cliente.telefone == telefone).first()

    def atualizar(self, cliente: Cliente) -> Cliente:
        """Atualiza um cliente existente."""
        try:
            self.session.merge(cliente)
            self.session.commit()
            return cliente
        except Exception as e:
            self.session.rollback()
            raise e

    def atualizar_por_id(self, id_cliente: int, nome: Optional[str] = None, cpf: Optional[str] = None,
                         telefone: Optional[str] = None) -> Optional[Cliente]:
        """Atualiza um cliente existente por ID."""
        try:
            cliente = self.buscar_por_id(id_cliente)
            if cliente:
                if nome is not None:
                    cliente.nome = nome
                if cpf is not None:
                    cliente.cpf = cpf
                if telefone is not None:
                    cliente.telefone = telefone

                self.session.commit()
                return cliente
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def deletar(self, id_cliente: int) -> bool:
        """Deleta um cliente pelo ID."""
        try:
            cliente = self.buscar_por_id(id_cliente)
            if cliente:
                self.session.delete(cliente)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def verificar_cpf_existe(self, cpf: str, id_cliente: Optional[int] = None) -> bool:
        """Verifica se um CPF já existe no banco (exceto para o próprio cliente)."""
        query = self.session.query(Cliente).filter(Cliente.cpf == cpf)
        if id_cliente:
            query = query.filter(Cliente.id_cliente != id_cliente)
        return query.first() is not None

    def fechar_sessao(self):
        """Fecha a sessão do banco de dados."""
        self.session.close()
