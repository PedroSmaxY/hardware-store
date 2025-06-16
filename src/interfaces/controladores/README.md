# Pasta Controladores

## Descrição

A pasta `controladores` implementa a camada de controle da interface gráfica do sistema de loja de ferragens, seguindo o padrão MVC (Model-View-Controller). Esta camada atua como intermediária entre as interfaces visuais (arquivos .ui) e a lógica de negócio (serviços), coordenando as interações do usuário e atualizando as views conforme necessário.

## Responsabilidades

### Principais Funções

- **Conexão View-Service**: Liga as interfaces gráficas aos serviços de negócio
- **Gerenciamento de Eventos**: Captura e processa eventos da interface (cliques, digitação, etc.)
- **Validação de Interface**: Aplica validações visuais antes de enviar dados aos serviços
- **Atualização de Views**: Atualiza elementos da interface baseado em respostas dos serviços
- **Navegação**: Controla a navegação entre diferentes telas do sistema

### Estrutura dos Controladores

Cada controlador corresponde a uma tela específica e gerencia:

- Inicialização da interface
- Conexão de sinais e slots do PyQt6
- Preenchimento de dados nas views
- Validação de formulários
- Chamadas aos serviços apropriados
- Tratamento de erros e feedback ao usuário

## Padrões Utilizados

- **MVC Pattern**: Separação clara entre Model (serviços), View (telas) e Controller
- **Event-Driven**: Programação orientada a eventos do PyQt6
- **Dependency Injection**: Injeção dos serviços necessários nos controladores
- **Single Responsibility**: Cada controlador gerencia uma tela específica

## Funcionalidades Comuns

- **Validação de Formulários**: Verificação de campos obrigatórios e formatos
- **Feedback Visual**: Exibição de mensagens de sucesso, erro e avisos
- **Carregamento de Dados**: População de tabelas, comboboxes e listas
- **Navegação**: Abertura e fechamento de janelas
- **Estado da Interface**: Habilitação/desabilitação de componentes

## Dependências

- `PyQt6`: Framework de interface gráfica
- `src.servicos`: Camada de lógica de negócio
- `src.interface.telas`: Arquivos de interface (.ui)

## Uso

Os controladores são instanciados pela aplicação principal e conectam automaticamente:

- Eventos da interface aos métodos de controle
- Métodos de controle aos serviços de negócio
- Respostas dos serviços às atualizações da interface

## Exemplo de Fluxo

1. Usuário clica em um botão na interface
2. Controlador captura o evento
3. Controlador valida dados se necessário
4. Controlador chama o serviço apropriado
5. Controlador processa a resposta do serviço
6. Controlador atualiza a interface com o resultado
