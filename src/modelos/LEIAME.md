# Pasta Modelos

## Descrição

A pasta `modelos` contém as definições dos modelos de dados (ORM) do sistema de loja de hardware, utilizando SQLAlchemy com Mapped Classes. Esta pasta implementa a camada de persistência, definindo a estrutura das tabelas do banco de dados e seus relacionamentos conforme o diagrama de entidades do sistema.

## Arquivos

### `tabelas_bd.py`

- **Propósito**: Definição dos modelos de dados ORM
- **Funcionalidades**:
  - Implementação das classes que representam as tabelas do banco
  - Definição de colunas, tipos de dados e constraints
  - Configuração de relacionamentos entre entidades
  - Métodos `__repr__` para representação dos objetos

## Classes/Entidades

### `Produto`

- **Atributos**: id_produto, nome, descricao, quantidade_estoque, preco
- **Relacionamentos**: Um produto pode estar em muitos itens de venda

### `Cliente`

- **Atributos**: id_cliente, nome, cpf, telefone
- **Relacionamentos**: Um cliente pode ter muitas vendas

### `Funcionario`

- **Atributos**: id_funcionario, nome, cargo, nome_usuario, senha
- **Relacionamentos**: Um funcionário pode realizar muitas vendas
- **Enum**: CargoEnum (GERENTE, VENDEDOR, ESTOQUISTA)

### `Venda`

- **Atributos**: id_venda, data_venda, id_funcionario, id_cliente, valor_total
- **Relacionamentos**: Pertence a um funcionário e opcionalmente a um cliente; possui muitos itens

### `ItensVenda`

- **Atributos**: id_item_venda, id_venda, id_produto, quantidade, preco_unitario, desconto_aplicado
- **Relacionamentos**: Pertence a uma venda e referencia um produto

## Padrões Utilizados

- **ORM (Object-Relational Mapping)**: Mapeamento objeto-relacional com SQLAlchemy
- **Mapped Classes**: Uso de anotações de tipo para definição de colunas
- **Relacionamentos Bidirecionais**: Configuração de relacionamentos entre entidades
- **Enum**: Utilização de enums para campos com valores pré-definidos
- **Constraints**: Definição de chaves primárias, estrangeiras e campos únicos

## Dependências

- `SQLAlchemy`: Framework ORM
- `typing`: Suporte a anotações de tipo
- `enum`: Definição de enumerações

## Uso

Os modelos desta pasta são utilizados por:

- Repositórios para operações CRUD
- Serviços para aplicação de regras de negócio
- Migrações e inicialização do banco de dados
- Validação e serialização de dados
