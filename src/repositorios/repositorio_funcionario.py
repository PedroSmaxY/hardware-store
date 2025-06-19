from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.configs.config_bd import Session as SessionLocal
from src.modelos.tabelas_bd import Funcionario
from src.modelos.tabelas_bd import CargoEnum

"""
Este arquivo implementa o repositório para operações CRUD da entidade Funcionario,
seguindo o padrão Repository. Encapsula todas as operações de acesso a dados
relacionadas aos funcionários, incluindo autenticação e controle de acesso,
fornecendo uma camada de abstração entre o modelo de dados e a lógica de negócio.
"""


class FuncionarioRepositorio:
    """Repositório para operações CRUD da entidade Funcionario."""

    def __init__(self, session: Session | None = None):
        self.session = session or SessionLocal()

    def salvar(self, funcionario: Funcionario) -> Funcionario:
        """Salva um funcionário no banco de dados."""
        try:
            self.session.add(funcionario)
            self.session.commit()
            self.session.refresh(funcionario)
            return funcionario
        except Exception as e:
            self.session.rollback()
            raise e

    def criar(self, nome: str, nome_usuario: str, senha_hash: str, cargo: CargoEnum) -> Funcionario:
        """Cria um novo funcionário no banco de dados."""
        try:
            funcionario = Funcionario(
                nome=nome,
                nome_usuario=nome_usuario,
                senha_hash=senha_hash,
                cargo=cargo
            )
            self.session.add(funcionario)
            self.session.commit()
            self.session.refresh(funcionario)
            return funcionario
        except Exception as e:
            self.session.rollback()
            raise e

    def buscar_por_id(self, id_funcionario: int) -> Optional[Funcionario]:
        """Busca um funcionário pelo ID."""
        return self.session.query(Funcionario).filter(Funcionario.id_funcionario == id_funcionario).first()

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

    def buscar_por_nome(self, nome: str) -> List[Funcionario]:
        """Busca funcionários pelo nome (busca parcial)."""
        return self.session.query(Funcionario).filter(
            Funcionario.nome.ilike(f"%{nome}%")
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

    def atualizar_por_id(self, id_funcionario: int, nome: Optional[str] = None,
                         nome_usuario: Optional[str] = None, senha_hash: Optional[str] = None,
                         cargo: Optional[CargoEnum] = None) -> Optional[Funcionario]:
        """Atualiza um funcionário existente por ID."""
        try:
            funcionario = self.buscar_por_id(id_funcionario)
            if funcionario:
                if nome is not None:
                    funcionario.nome = nome
                if nome_usuario is not None:
                    funcionario.nome_usuario = nome_usuario
                if senha_hash is not None:
                    funcionario.senha_hash = senha_hash
                if cargo is not None:
                    funcionario.cargo = cargo

                self.session.commit()
                return funcionario
            return None
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

    def autenticar(self, nome_usuario: str, senha_hash: str) -> Optional[Funcionario]:
        """Autentica um funcionário pelo nome de usuário e senha hash."""
        return self.session.query(Funcionario).filter(
            and_(
                Funcionario.nome_usuario == nome_usuario,
                Funcionario.senha_hash == senha_hash
            )
        ).first()

    def verificar_nome_usuario_existe(self, nome_usuario: str, id_funcionario: Optional[int] = None) -> bool:
        """Verifica se um nome de usuário já existe no banco (exceto para o próprio funcionário)."""
        query = self.session.query(Funcionario).filter(
            Funcionario.nome_usuario == nome_usuario)
        if id_funcionario:
            query = query.filter(Funcionario.id_funcionario != id_funcionario)
        return query.first() is not None

    def contar_funcionarios_por_cargo(self, cargo: CargoEnum) -> int:
        """Conta quantos funcionários existem de um cargo específico."""
        return self.session.query(Funcionario).filter(Funcionario.cargo == cargo).count()

    def fechar_sessao(self):
        """Fecha a sessão do banco de dados."""
        self.session.close()
