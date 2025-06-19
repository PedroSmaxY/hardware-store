from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from src.configs.config_bd import Session as SessionLocal
from src.modelos.tabelas_bd import Venda, ItensVenda

"""
Este arquivo implementa o repositório para operações CRUD da entidade Venda,
seguindo o padrão Repository. Encapsula todas as operações de acesso a dados
relacionadas às vendas, fornecendo uma camada de abstração entre o modelo
de dados e a lógica de negócio da aplicação.
"""


class VendaRepositorio:
    """Repositório para operações CRUD da entidade Venda."""

    def __init__(self, session: Session | None = None):
        self.session = session or SessionLocal()

    def salvar(self, venda: Venda) -> Venda:
        """Salva uma venda no banco de dados."""
        try:
            self.session.add(venda)
            self.session.commit()
            self.session.refresh(venda)
            return venda
        except Exception as e:
            self.session.rollback()
            raise e

    def criar(self, data_venda: datetime, id_funcionario: int,
              id_cliente: Optional[int] = None, valor_total: float = 0.0,
              desconto_aplicado: float = 0.0) -> Venda:
        """Cria uma nova venda no banco de dados."""
        try:
            venda = Venda(
                data_venda=data_venda,
                id_funcionario=id_funcionario,
                id_cliente=id_cliente,
                valor_total=valor_total,
                desconto_aplicado=desconto_aplicado
            )
            self.session.add(venda)
            self.session.commit()
            self.session.refresh(venda)
            return venda
        except Exception as e:
            self.session.rollback()
            raise e

    def buscar_por_id(self, id_venda: int) -> Optional[Venda]:
        """Busca uma venda pelo ID."""
        return self.session.query(Venda).filter(Venda.id_venda == id_venda).first()

    def buscar_todos(self) -> List[Venda]:
        """Busca todas as vendas."""
        return self.session.query(Venda).all()

    def buscar_por_funcionario(self, id_funcionario: int) -> List[Venda]:
        """Busca todas as vendas de um funcionário específico."""
        return self.session.query(Venda).filter(
            Venda.id_funcionario == id_funcionario
        ).all()

    def buscar_por_cliente(self, id_cliente: int) -> List[Venda]:
        """Busca todas as vendas de um cliente específico."""
        return self.session.query(Venda).filter(
            Venda.id_cliente == id_cliente
        ).all()

    def buscar_por_periodo(self, data_inicio: datetime, data_fim: datetime) -> List[Venda]:
        """Busca vendas em um período específico."""
        return self.session.query(Venda).filter(
            and_(
                Venda.data_venda >= data_inicio,
                Venda.data_venda <= data_fim
            )
        ).all()

    def buscar_por_data(self, data: datetime) -> List[Venda]:
        """Busca vendas de uma data específica."""
        data_inicio = data.replace(hour=0, minute=0, second=0, microsecond=0)
        data_fim = data.replace(
            hour=23, minute=59, second=59, microsecond=999999)

        return self.session.query(Venda).filter(
            and_(
                Venda.data_venda >= data_inicio,
                Venda.data_venda <= data_fim
            )
        ).all()

    def buscar_vendas_recentes(self, limite: int = 10) -> List[Venda]:
        """Busca as vendas mais recentes."""
        return self.session.query(Venda).order_by(
            Venda.data_venda.desc()
        ).limit(limite).all()

    def buscar_vendas_acima_valor(self, valor_minimo: float) -> List[Venda]:
        """Busca vendas com valor total acima de um valor mínimo."""
        return self.session.query(Venda).filter(
            Venda.valor_total >= valor_minimo
        ).all()

    def atualizar(self, venda: Venda) -> Venda:
        """Atualiza uma venda existente."""
        try:
            self.session.merge(venda)
            self.session.commit()
            return venda
        except Exception as e:
            self.session.rollback()
            raise e

    def atualizar_por_id(self, id_venda: int, data_venda: Optional[datetime] = None,
                         id_funcionario: Optional[int] = None, id_cliente: Optional[int] = None,
                         valor_total: Optional[float] = None, desconto_aplicado: Optional[float] = None) -> Optional[Venda]:
        """Atualiza uma venda existente por ID."""
        try:
            venda = self.buscar_por_id(id_venda)
            if venda:
                if data_venda is not None:
                    venda.data_venda = data_venda
                if id_funcionario is not None:
                    venda.id_funcionario = id_funcionario
                if id_cliente is not None:
                    venda.id_cliente = id_cliente
                if valor_total is not None:
                    venda.valor_total = valor_total
                if desconto_aplicado is not None:
                    venda.desconto_aplicado = desconto_aplicado

                self.session.commit()
                return venda
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def deletar(self, id_venda: int) -> bool:
        """Deleta uma venda pelo ID."""
        try:
            venda = self.buscar_por_id(id_venda)
            if venda:
                # Remove primeiro todos os itens da venda
                self.session.query(ItensVenda).filter(
                    ItensVenda.id_venda == id_venda
                ).delete()

                # Remove a venda
                self.session.delete(venda)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def contar_vendas(self) -> int:
        """Conta o total de vendas."""
        return self.session.query(Venda).count()

    def contar_vendas_por_funcionario(self, id_funcionario: int) -> int:
        """Conta o número de vendas de um funcionário específico."""
        return self.session.query(Venda).filter(
            Venda.id_funcionario == id_funcionario
        ).count()

    def contar_vendas_por_cliente(self, id_cliente: int) -> int:
        """Conta o número de vendas de um cliente específico."""
        return self.session.query(Venda).filter(
            Venda.id_cliente == id_cliente
        ).count()

    def contar_vendas_periodo(self, data_inicio: datetime, data_fim: datetime) -> int:
        """Conta vendas em um período específico."""
        return self.session.query(Venda).filter(
            and_(
                Venda.data_venda >= data_inicio,
                Venda.data_venda <= data_fim
            )
        ).count()

    def calcular_total_vendas(self) -> float:
        """Calcula o valor total de todas as vendas."""
        resultado = self.session.query(func.sum(Venda.valor_total)).scalar()
        return float(resultado) if resultado else 0.0

    def calcular_total_vendas_funcionario(self, id_funcionario: int) -> float:
        """Calcula o valor total de vendas de um funcionário específico."""
        resultado = self.session.query(func.sum(Venda.valor_total)).filter(
            Venda.id_funcionario == id_funcionario
        ).scalar()
        return float(resultado) if resultado else 0.0

    def calcular_total_vendas_cliente(self, id_cliente: int) -> float:
        """Calcula o valor total de vendas de um cliente específico."""
        resultado = self.session.query(func.sum(Venda.valor_total)).filter(
            Venda.id_cliente == id_cliente
        ).scalar()
        return float(resultado) if resultado else 0.0

    def calcular_total_vendas_periodo(self, data_inicio: datetime, data_fim: datetime) -> float:
        """Calcula o valor total de vendas em um período."""
        resultado = self.session.query(func.sum(Venda.valor_total)).filter(
            and_(
                Venda.data_venda >= data_inicio,
                Venda.data_venda <= data_fim
            )
        ).scalar()
        return float(resultado) if resultado else 0.0

    def calcular_media_valor_vendas(self) -> float:
        """Calcula a média do valor das vendas."""
        resultado = self.session.query(func.avg(Venda.valor_total)).scalar()
        return float(resultado) if resultado else 0.0

    def calcular_total_descontos(self) -> float:
        """Calcula o valor total de descontos aplicados."""
        resultado = self.session.query(
            func.sum(Venda.desconto_aplicado)).scalar()
        return float(resultado) if resultado else 0.0

    def buscar_maior_venda(self) -> Optional[Venda]:
        """Busca a venda com maior valor."""
        return self.session.query(Venda).order_by(
            Venda.valor_total.desc()
        ).first()

    def buscar_menor_venda(self) -> Optional[Venda]:
        """Busca a venda com menor valor."""
        return self.session.query(Venda).order_by(
            Venda.valor_total.asc()
        ).first()

    def buscar_vendas_sem_cliente(self) -> List[Venda]:
        """Busca vendas que não possuem cliente associado."""
        return self.session.query(Venda).filter(
            Venda.id_cliente.is_(None)
        ).all()

    def buscar_vendas_com_desconto(self) -> List[Venda]:
        """Busca vendas que tiveram desconto aplicado."""
        return self.session.query(Venda).filter(
            Venda.desconto_aplicado > 0
        ).all()

    def obter_relatorio_vendas_diario(self, data: datetime) -> dict:
        """Gera relatório de vendas do dia."""
        vendas_dia = self.buscar_por_data(data)

        total_vendas = len(vendas_dia)
        valor_total = sum(venda.valor_total for venda in vendas_dia)
        total_descontos = sum(
            venda.desconto_aplicado or 0 for venda in vendas_dia)

        return {
            "data": data.strftime("%Y-%m-%d"),
            "total_vendas": total_vendas,
            "valor_total": valor_total,
            "total_descontos": total_descontos,
            "valor_medio_venda": valor_total / total_vendas if total_vendas > 0 else 0,
            "vendas": vendas_dia
        }

    def obter_ranking_funcionarios(self, data_inicio: datetime, data_fim: datetime) -> List[dict]:
        """Obtém ranking de funcionários por vendas em um período."""
        resultado = self.session.query(
            Venda.id_funcionario,
            func.count(Venda.id_venda).label('total_vendas'),
            func.sum(Venda.valor_total).label('valor_total')
        ).filter(
            and_(
                Venda.data_venda >= data_inicio,
                Venda.data_venda <= data_fim
            )
        ).group_by(Venda.id_funcionario).order_by(
            func.sum(Venda.valor_total).desc()
        ).all()

        return [
            {
                "id_funcionario": r.id_funcionario,
                "total_vendas": r.total_vendas,
                "valor_total": float(r.valor_total)
            }
            for r in resultado
        ]

    def fechar_sessao(self):
        """Fecha a sessão do banco de dados."""
        self.session.close()
