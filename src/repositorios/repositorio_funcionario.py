from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.configs.config_bd import Session as SessionLocal
from src.modelos.tabelas_bd import Funcionario
from src.modelos.tabelas_bd import CargoEnum


class FuncionarioRepositorio:
    """Repositório para operações CRUD da entidade Funcionario."""

    def __init__(self, session: Session | None = None):
        self.session = session or SessionLocal()

    def criar(self, funcionario: Funcionario) -> Funcionario:
        """Cria um novo funcionário no banco de dados."""
        try:
            self.session.add(funcionario)
            self.session.commit()
            self.session.refresh(funcionario)
            return funcionario
        except Exception as e:
            self.session.rollback()
            raise e

    def buscar_por_id(self, id_funcionario: int) -> Optional[Funcionario]:
        """Busca um funcionário pelo ID."""
        return self.session.query(Funcionario).filter(Funcionario.id == id_funcionario).first()

    def buscar_todos(self) -> List[Funcionario]:
        """Retorna todos os funcionários cadastrados."""
        return self.session.query(Funcionario).all()

    def buscar_por_nome_usuario(self, nome_usuario: str) -> Optional[Funcionario]:
        """Busca um funcionário pelo nome de usuário."""
        return self.session.query(Funcionario).filter(
            Funcionario.nome_usuario == nome_usuario
        ).first()

    def buscar_por_cargo(self, cargo: CargoEnum) -> List[Funcionario]:
        """Busca funcionários pelo cargo."""
        return self.session.query(Funcionario).filter(
            Funcionario.cargo == cargo
        ).all()

    def atualizar(self, funcionario: Funcionario) -> Funcionario:
        """Atualiza um funcionário existente."""
        try:
            self.session.merge(funcionario)
            self.session.commit()
            return funcionario
        except Exception as e:
            self.session.rollback()
            raise e

    def deletar(self, id_funcionario: int) -> bool:
        """Deleta um funcionário pelo ID."""
        try:
            funcionario = self.buscar_por_id(id_funcionario)
            if funcionario:
                self.session.delete(funcionario)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def autenticar(self, nome_usuario: str, senha: str) -> Optional[Funcionario]:
        """Autentica um funcionário pelo nome de usuário e senha."""
        return self.session.query(Funcionario).filter(
            and_(
                Funcionario.nome_usuario == nome_usuario,
                Funcionario.senha == senha
            )
        ).first()
