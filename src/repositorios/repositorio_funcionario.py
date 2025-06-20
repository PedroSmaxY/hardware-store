from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from contextlib import contextmanager
from src.configs.config_bd import Session as SessionLocal
from src.modelos.tabelas_bd import Funcionario
from src.modelos.tabelas_bd import CargoEnum

class FuncionarioRepositorio:
    """Repositório para operações CRUD da entidade Funcionario."""

    @contextmanager
    def session_scope(self):
        """
        Gerencia o ciclo de vida da sessão: cria, executa, faz commit ou rollback e fecha.
        Garante segurança transacional e liberação correta de recursos. (Basicamente EVITA o ERRO de DATABASE IS LOCKED)
        """
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def salvar(self, funcionario: Funcionario) -> Funcionario:
        """
        Salva um funcionário na base de dados, adicionando e sincronizando seu estado.
        """
        with self.session_scope() as session:
            session.add(funcionario)
            session.flush()
            session.refresh(funcionario)
            return funcionario

    def criar(self, nome: str, nome_usuario: str, senha_hash: str, cargo: CargoEnum) -> Funcionario:
        """
        Instancia um novo funcionário com os dados fornecidos e salva no banco.
        """
        with self.session_scope() as session:
            funcionario = Funcionario(
                nome=nome,
                nome_usuario=nome_usuario,
                senha_hash=senha_hash,
                cargo=cargo
            )
            session.add(funcionario)
            session.flush()
            session.refresh(funcionario)
            return funcionario

    def buscar_por_id(self, id_funcionario: int) -> Optional[Funcionario]:
        """
        Busca um funcionário pelo seu ID
        """
        with SessionLocal() as session:
            return session.query(Funcionario).filter(Funcionario.id_funcionario == id_funcionario).first()

    def buscar_todos(self) -> List[Funcionario]:
        """
        Busca todos os funcionários presentes no sistema.
        """
        with SessionLocal() as session:
            return session.query(Funcionario).all()

    def buscar_por_nome_usuario(self, nome_usuario: str) -> Optional[Funcionario]:
        """
        Busca um funcionário pelo nome de usuário.
        """
        with SessionLocal() as session:
            return session.query(Funcionario).filter(
                Funcionario.nome_usuario == nome_usuario
            ).first()

    def buscar_por_cargo(self, cargo: CargoEnum) -> List[Funcionario]:
        """
        Busca todos os funcionários que possuem um cargo específico.
        """
        with SessionLocal() as session:
            return session.query(Funcionario).filter(
                Funcionario.cargo == cargo
            ).all()

    def buscar_por_nome(self, nome: str) -> List[Funcionario]:
        """
        Busca um funcionário pelo seu nome.
        """
        with SessionLocal() as session:
            return session.query(Funcionario).filter(
                Funcionario.nome.ilike(f"%{nome}%")
            ).all()

    def atualizar(self, funcionario: Funcionario) -> Funcionario:
        """
        Atualiza os dados de um funcionário já existente e sincroniza as mudanças.
        """
        with self.session_scope() as session:
            funcionario = session.merge(funcionario)
            session.flush()
            return funcionario

    def atualizar_por_id(self, id_funcionario: int, nome: Optional[str] = None,
                         nome_usuario: Optional[str] = None, senha_hash: Optional[str] = None,
                         cargo: Optional[CargoEnum] = None) -> Optional[Funcionario]:
        """
        Busca o funcionário pelo ID e atualiza os campos informados, salvando as mudanças.
        """
        with self.session_scope() as session:
            funcionario = session.query(Funcionario).filter(Funcionario.id_funcionario == id_funcionario).first()
            if funcionario:
                if nome is not None:
                    funcionario.nome = nome
                if nome_usuario is not None:
                    funcionario.nome_usuario = nome_usuario
                if senha_hash is not None:
                    funcionario.senha_hash = senha_hash
                if cargo is not None:
                    funcionario.cargo = cargo
                session.flush()
                return funcionario
            return None

    def deletar(self, id_funcionario: int) -> bool:
        """
        Remove o funcionário identificado pelo ID da base de dados.
        Retorna True se a exclusão foi realizada, False caso contrário.
        """
        with self.session_scope() as session:
            funcionario = session.query(Funcionario).filter(Funcionario.id_funcionario == id_funcionario).first()
            if funcionario:
                session.delete(funcionario)
                return True
            return False

    def autenticar(self, nome_usuario: str, senha_hash: str) -> Optional[Funcionario]:
        """
        Consulta o funcionário que possui o nome de usuário e hash de senha informados para que possibilita que ele entre no sistema.
        """
        with SessionLocal() as session:
            return session.query(Funcionario).filter(
                and_(
                    Funcionario.nome_usuario == nome_usuario,
                    Funcionario.senha_hash == senha_hash
                )
            ).first()

    def verificar_nome_usuario_existe(self, nome_usuario: str, id_funcionario: Optional[int] = None) -> bool:
        """
        Verifica a existência de um nome de usuário no sistema,
        Para evitar repetição na criação de usuários novos.
        """
        with SessionLocal() as session:
            query = session.query(Funcionario).filter(Funcionario.nome_usuario == nome_usuario)
            if id_funcionario:
                query = query.filter(Funcionario.id_funcionario != id_funcionario)
            return query.first() is not None

    def contar_funcionarios_por_cargo(self, cargo: CargoEnum) -> int:
        """
        Retorna o total de funcionários cadastrados para o cargo informado.
        """
        with SessionLocal() as session:
            return session.query(Funcionario).filter(Funcionario.cargo == cargo).count()
