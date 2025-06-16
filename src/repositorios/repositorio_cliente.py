from typing import List, Optional
from sqlalchemy.orm import Session
from src.configs.config_bd import Session as SessionLocal
from src.modelos.tabelas_bd import Cliente


class ClienteRepositorio:
    """Repositório para operações CRUD da entidade Cliente."""

    def __init__(self, session: Session | None = None):
        self.session = session or SessionLocal()

    def criar(self, cliente: Cliente) -> Cliente:
        """Cria um novo cliente no banco de dados."""
        try:
            self.session.add(cliente)
            self.session.commit()
            self.session.refresh(cliente)
            return cliente
        except Exception as e:
            self.session.rollback()
            raise e

    def buscar_por_id(self, id_cliente: int) -> Optional[Cliente]:
        """Busca um cliente pelo ID."""
        return self.session.query(Cliente).filter(Cliente.id == id_cliente).first()

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

    def atualizar(self, cliente: Cliente) -> Cliente:
        """Atualiza um cliente existente."""
        try:
            self.session.merge(cliente)
            self.session.commit()
            return cliente
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
