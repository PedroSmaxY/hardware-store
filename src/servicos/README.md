# Pasta Serviços

## Descrição

A pasta `servicos` implementa o padrão Service Layer para encapsular a lógica de negócio do sistema de loja de hardware. Esta camada coordena operações entre repositórios, aplica regras de negócio específicas e fornece uma interface de alto nível para as operações do sistema, mantendo a separação entre a lógica de negócio e o acesso aos dados.

## Arquivos

### `servicos_bd.py`

- **Propósito**: Implementação das classes de serviço para cada entidade
- **Funcionalidades**:
  - Aplicação de regras de negócio específicas
  - Coordenação de operações entre múltiplos repositórios
  - Validações de dados e integridade
  - Processamento de transações complexas

## Classes de Serviço

### `ProdutoServico`

- **Responsabilidades**: Gestão de produtos e controle de estoque
- **Regras de Negócio**:
  - Validação de preços e quantidades
  - Controle de estoque disponível
  - Redução automática de estoque em vendas
  - Validação de dados de produto

### `ClienteServico`

- **Responsabilidades**: Gerenciamento de clientes
- **Regras de Negócio**:
  - Validação de CPF (formato e unicidade)
  - Verificação de dados obrigatórios
  - Controle de duplicatas
  - Formatação e normalização de dados

### `FuncionarioServico`

- **Responsabilidades**: Gestão de funcionários e autenticação
- **Regras de Negócio**:
  - Criptografia de senhas
  - Validação de credenciais de login
  - Controle de permissões por cargo
  - Verificação de unicidade de nome de usuário

### `VendaServico`

- **Responsabilidades**: Processamento de vendas e transações
- **Regras de Negócio**:
  - Cálculo automático de valor total
  - Validação de estoque antes da venda
  - Controle de status da venda
  - Integração com controle de estoque
  - Geração de relatórios de venda

### `ItensVendaServico`

- **Responsabilidades**: Gestão de itens individuais de vendas
- **Regras de Negócio**:
  - Cálculo de subtotais com descontos
  - Aplicação de promoções e descontos
  - Validação de quantidades disponíveis
  - Controle de preços no momento da venda

## Padrões Utilizados

- **Service Layer Pattern**: Encapsulamento da lógica de negócio
- **Dependency Injection**: Injeção de repositórios nas classes de serviço
- **Single Responsibility**: Cada serviço gerencia uma área específica do negócio
- **Transaction Script**: Coordenação de operações transacionais complexas

## Funcionalidades Comuns

- **Validação de Dados**: Verificação de integridade e consistência
- **Regras de Negócio**: Aplicação de políticas específicas do domínio
- **Coordenação**: Orquestração de operações entre múltiplas entidades
- **Tratamento de Erros**: Gestão de exceções de negócio
- **Segurança**: Validações de segurança e controle de acesso

## Dependências

- `typing`: Anotações de tipo para maior clareza
- `datetime`: Manipulação de datas e horários
- `src.repositorios.repositorios_bd`: Repositórios de acesso a dados
- `src.modelos.tabelas_bd`: Modelos de dados do sistema

## Uso

Os serviços são utilizados por:

- Controllers/Views para operações de interface
- APIs REST para endpoints de negócio
- Testes de integração para validação de regras
- Scripts de automação e processamento batch
- Interfaces de usuário (CLI, GUI, Web)
