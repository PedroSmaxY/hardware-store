# 🔧 Hardware Store - Sistema de Loja de Hardware

Sistema de gestão para loja de hardware desenvolvido em Python com SQLAlchemy e PyQt6, implementando padrões de arquitetura limpa com Repository e Service Layer para a disciplina de Laboratório de Desenvolvimento de Software.

## 📋 Descrição do Projeto

Este sistema permite o gerenciamento completo de uma loja de hardware, incluindo controle de estoque, cadastro de clientes e funcionários, processamento de vendas e geração de relatórios.

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas com separação clara de responsabilidades:

```
hardware-store/
├── start.py              # Ponto de entrada da aplicação
├── requirements.txt      # Dependências do projeto
├── .env                  # Variáveis de ambiente
└── src/
    ├── configs/          # Configurações de banco de dados e ambiente
    ├── modelos/          # Modelos ORM (SQLAlchemy)
    ├── repositorios/     # Camada de acesso a dados (Repository Pattern)
    ├── servicos/         # Lógica de negócio (Service Layer)
    └── interface/        # Interfaces gráficas (PyQt6)
        ├── telas/        # Arquivos .ui (Qt Designer)
        └── controladores/ # Lógica das telas (Python)
```

## 📦 Instalação e Configuração

### Método 1: Instalação do UV (Recomendado)

O UV é um gerenciador de pacotes Python ultra-rápido, escrito em Rust.

#### No macOS/Linux:

```bash
# Instalação via curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Ou via Homebrew (macOS)
brew install uv
```

#### No Windows:

```bash
# Via PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Ou via Scoop
scoop install uv
```

### Etapa 2: Configuração do Projeto com UV

```bash
# 1. Clone o repositório
git clone https://github.com/PedroSmaxY/hardware-store.git
cd hardware-store

# 2. Sincronize as dependências e crie o ambiente virtual automaticamente
uv sync

# 3. Execute o projeto
uv run start.py
```

Para mais informações sobre o UV: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

### Método 3: Instalação Tradicional (pip)

```bash
# 1. Crie um ambiente virtual
python -m venv venv

# 2. Ative o ambiente virtual
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o projeto
python start.py
```

## 🚀 Como Executar o Projeto

Após seguir os passos de instalação acima:

```bash
# Com UV
uv run start.py

# Ou com Python tradicional (ambiente virtual ativado)
python start.py
```

## 🔧 Configuração do Ambiente

### Arquivo .env

Crie um arquivo `.env` na raiz do projeto com as configurações necessárias:

```env
# Para SQLite (padrão - criado automaticamente)
URL_BANCO_DE_DADOS=sqlite:///hardware_store.db

# Para MySQL (substitua pelos seus dados)
URL_BANCO_DE_DADOS=mysql+pymysql://usuario:senha@localhost:3306/hardware_store?charset=utf8mb4

# Exemplo prático:
URL_BANCO_DE_DADOS=mysql+pymysql://root:minhasenha@localhost:3306/hardware_store?charset=utf8mb4
```

**Nota**: O sistema criará automaticamente o banco de dados e as tabelas na primeira execução.

**Dica**: Você pode copiar o arquivo `.env.exemplo` como base e renomeá-lo para `.env`.

## 📚 Stack Tecnológica

- **Python**: Linguagem principal do projeto
- **SQLAlchemy**: ORM para mapeamento objeto-relacional
- **PyQt6**: Framework para interface gráfica
- **SQLite/MySQL**: Banco de dados (configurável)
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 🛠️ Funcionalidades do Sistema

O sistema oferece uma solução completa para gestão de loja de hardware, incluindo controle de estoque, cadastro de clientes e funcionários, processamento de vendas e geração de relatórios.

## 🎨 Interface Gráfica

### Organização da Interface

- **telas/**: Contém os arquivos `.ui` criados no Qt Designer
- **controladores/**: Contém a lógica Python que conecta as telas aos serviços

## 🏫 Contexto Acadêmico

Este projeto foi desenvolvido para a disciplina de **Laboratório de Desenvolvimento de Software**, demonstrando:

- **Padrões de Design**: Repository, Service Layer
- **Arquitetura Limpa**: Separação clara de responsabilidades
- **Interface Gráfica**: Desenvolvimento com PyQt6 e Qt Designer
- **Persistência de Dados**: ORM com SQLAlchemy
- **Boas Práticas**: Documentação, estrutura de pastas, validações

## 👥 Equipe de Desenvolvimento

- **Disciplina**: Laboratório de Desenvolvimento de Software
- **Curso**: Ciência da Computação
- **Instituição**: Universidade Veiga de Almeida (UVA)

**Desenvolvedores**:

- Pedro Henrique Novais - [GitHub](https://github.com/PedroSmaxY)
- Victor Jacques Freire Sampaio - [GitHub](https://github.com/Victor-Jacques)
- Diego Tasso da Cunha Ferreira - [GitHub](https://github.com/diegotassodev)
-

---

  **Tecnologias Utilizadas**: Python • PyQt6 • SQLAlchemy • SQLite/MySQL  
  **Padrões**: Repository Pattern • Service Layer
