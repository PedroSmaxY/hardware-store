# Pasta Telas

## Descrição

A pasta `telas` contém os arquivos de interface gráfica (.ui) criados no Qt Designer para o sistema de loja de hardware. Esta pasta representa a camada View do padrão MVC, definindo a estrutura visual das interfaces que serão controladas pelos controladores Python.

## Conteúdo

### Arquivos .ui

- **Formato**: XML gerado pelo Qt Designer
- **Conteúdo**: Layout, widgets, propriedades visuais e organização dos componentes
- **Propósito**: Definir a aparência e estrutura das telas do sistema

### Tipos de Interface

- **Formulários**: Entrada e edição de dados
- **Listagens**: Exibição de dados em tabelas
- **Dashboards**: Visão geral e métricas
- **Diálogos**: Confirmações e alertas

## Características

- **Separação**: Design visual independente da lógica de programação
- **Ferramenta**: Criados no Qt Designer (editor visual)
- **Carregamento**: Arquivos são carregados pelos controladores Python
- **Manutenção**: Mudanças visuais sem necessidade de alterar código

## Fluxo de Trabalho

1. Criar interface no Qt Designer
2. Salvar como arquivo .ui
3. Carregar no controlador Python
4. Conectar eventos e exibir ao usuário

## Vantagens

- **Prototipagem rápida** sem programação
- **Facilidade de manutenção** visual
- **Consistência** no design
- **Colaboração** entre designers e desenvolvedores
