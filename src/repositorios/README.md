# Pasta Repositórios

## Descrição

A pasta `repositorios` implementa o padrão Repository para acesso aos dados do sistema de loja de ferragens. Esta camada fornece uma abstração entre os modelos de dados e a lógica de negócio, encapsulando todas as operações CRUD (Create, Read, Update, Delete) e consultas específicas ao banco de dados.

## Arquivos

### `repositorio_produto.py`
- **Propósito**: Operações CRUD e consultas específicas para produtos
- **Funcionalidades**: Busca por nome/categoria, controle de estoque, produtos com estoque baixo

### `repositorio_cliente.py`
- **Propósito**: Gerenciamento completo de clientes
- **Funcionalidades**: Busca por CPF/email/telefone, validação de duplicatas, contagem de clientes

### `repositorio_funcionario.py`
- **Propósito**: Gestão de funcionários e autenticação
- **Funcionalidades**: Autenticação, controle de acesso, busca por cargo, ativação/desativação

### `repositorio_itens_venda.py`
- **Propósito**: Controle de itens de vendas e cálculos
- **Funcionalidades**: Cálculo de totais, produtos mais vendidos, quantidade vendida por produto

## Classes de Repositório

### `ProdutoRepositorio`
- **Operações CRUD**: Criar, buscar, atualizar e deletar produtos
- **Consultas Específicas**:
  - Busca por nome e categoria
  - Produtos com estoque baixo
  - Atualização, redução e aumento de estoque

### `ClienteRepositorio`
- **Operações CRUD**: Gerenciamento completo de clientes
- **Consultas Específicas**:
  - Busca por CPF, email e telefone (únicos)
  - Busca por nome (parcial)
  - Validação de CPF e email existentes

### `FuncionarioRepositorio`
- **Operações CRUD**: Gestão de funcionários
- **Consultas Específicas**:
  - Autenticação por nome de usuário e senha
  - Busca por cargo e funcionários ativos
  - Ativação/desativação e alteração de senha

### `ItensVendaRepositorio`
- **Operações CRUD**: Gerenciamento de itens de venda
- **Consultas Específicas**:
  - Cálculo de totais e subtotais
  - Produtos mais vendidos
  - Quantidade vendida por produto
  - Criação de múltiplos itens

## Padrões Utilizados

- **Repository Pattern**: Encapsulamento de lógica de acesso a dados
- **Dependency Injection**: Injeção de dependência de sessão SQLAlchemy
- **Single Responsibility**: Cada repositório cuida de uma entidade específica
- **Separation of Concerns**: Separação clara entre acesso a dados e lógica de negócio

## Funcionalidades Comuns

- **Gerenciamento de Sessão**: Controle automático de sessões do banco
- **Tratamento de Erros**: Rollback automático em caso de exceções
- **Transações**: Suporte a operações transacionais seguras
- **Consultas Otimizadas**: Queries eficientes com filtros e agregações

## Dependências

- `SQLAlchemy`: ORM e gerenciamento de sessões
- `typing`: Anotações de tipo para maior clareza
- `src.modelos.tabelas_bd`: Modelos de dados do sistema
- `src.configs.config_bd`: Configurações de banco de dados

## Uso

Os repositórios são utilizados por:

- Classes de serviço para aplicar regras de negócio
- Controladores