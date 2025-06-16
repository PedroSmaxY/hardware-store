# Pasta Repositórios

## Descrição

A pasta `repositorios` implementa o padrão Repository para acesso aos dados do sistema de loja de hardware. Esta camada fornece uma abstração entre os modelos de dados e a lógica de negócio, encapsulando todas as operações CRUD (Create, Read, Update, Delete) e consultas específicas ao banco de dados.

## Arquivos

### `repositorios_bd.py`

- **Propósito**: Implementação das classes de repositório para cada entidade
- **Funcionalidades**:
  - Operações CRUD padronizadas para todas as entidades
  - Consultas específicas e filtros customizados
  - Gerenciamento de sessões do SQLAlchemy
  - Abstração das operações de banco de dados

## Classes de Repositório

### `ProdutoRepositorio`

- **Operações CRUD**: Criar, buscar, atualizar e deletar produtos
- **Consultas Específicas**:
  - Busca por nome
  - Verificação de estoque
  - Atualização de quantidade em estoque

### `ClienteRepositorio`

- **Operações CRUD**: Gerenciamento completo de clientes
- **Consultas Específicas**:
  - Busca por CPF (único)
  - Busca por nome (parcial)
  - Validação de CPF existente

### `FuncionarioRepositorio`

- **Operações CRUD**: Gestão de funcionários
- **Consultas Específicas**:
  - Busca por nome de usuário
  - Filtragem por cargo
  - Autenticação de login

### `VendaRepositorio`

- **Operações CRUD**: Controle de vendas
- **Consultas Específicas**:
  - Vendas por funcionário
  - Vendas por cliente
  - Vendas por período de datas
  - Relatórios de vendas

### `ItensVendaRepositorio`

- **Operações CRUD**: Gerenciamento de itens de venda
- **Consultas Específicas**:
  - Itens por venda específica
  - Itens por produto
  - Cálculo de subtotais

## Padrões Utilizados

- **Repositorio Pattern**: Encapsulamento de lógica de acesso a dados
- **Dependency Injection**: Injeção de dependência de sessão SQLAlchemy
- **Single Responsibility**: Cada repositório cuida de uma entidade específica
- **Abstração**: Interface limpa entre dados e lógica de negócio

## Funcionalidades Comuns

- **Gerenciamento de Sessão**: Controle automático de sessões do banco
- **Tratamento de Erros**: Captura e tratamento de exceções de banco
- **Transações**: Suporte a operações transacionais
- **Consultas Otimizadas**: Queries eficientes com relacionamentos

## Dependências

- `SQLAlchemy`: ORM e gerenciamento de sessões
- `typing`: Anotações de tipo para maior clareza
- `src.modelos.tabelas_bd`: Modelos de dados do sistema
- `src.configs.config_bd`: Configurações de banco de dados

## Uso

Os repositórios são utilizados por:

- Classes de serviço para aplicar regras de negócio
- Controllers para operações diretas de dados
- Testes unitários para validação de persistência
- Scripts de migração e inicialização
