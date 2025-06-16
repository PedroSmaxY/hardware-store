# Pasta Configs

## Descrição

A pasta `configs` centraliza todas as configurações e definições de ambiente necessárias para o funcionamento do sistema de loja de hardware. Esta pasta segue o padrão de separação de responsabilidades, mantendo as configurações isoladas da lógica de negócio.

## Arquivos

### `config_bd.py`

- **Propósito**: Configuração e inicialização do banco de dados
- **Funcionalidades**:
  - Configuração da engine SQLAlchemy com SQLite ou MySQL
  - Criação da sessão de banco de dados
  - Definição da classe Base declarativa para ORM
  - Função para inicialização automática das tabelas

### `config_globais.py`

- **Propósito**: Gerenciamento de variáveis de ambiente e configurações globais
- **Funcionalidades**:
  - Carregamento de variáveis do arquivo `.env` usando python-dotenv
  - Centralização de configurações sensíveis (URLs, chaves, etc.)
  - Fornecimento de acesso padronizado às configurações do sistema

## Padrões Utilizados

- **Separação de Responsabilidades**: Cada arquivo tem uma responsabilidade específica
- **Configuração Centralizada**: Todas as configurações ficam em um local conhecido
- **Segurança**: Variáveis sensíveis são carregadas de arquivos de ambiente
- **Flexibilidade**: Facilita mudanças de configuração sem alteração de código

## Dependências

- `SQLAlchemy`: ORM para gerenciamento do banco de dados
- `python-dotenv`: Carregamento de variáveis de ambiente

## Uso

Os módulos desta pasta são importados por outras camadas da aplicação (repositórios, serviços, etc.) para acessar as configurações necessárias de forma centralizada e consistente.
