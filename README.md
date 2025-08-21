# Sistema de Contagem de Estoque

## Descrição
Sistema web completo para contagem de estoque com funcionalidades de busca de produtos, registro de lotes, controle de duplicação e geração de relatórios.

## Funcionalidades Principais

### 1. Busca de Produtos
- Busca produtos pelo código
- Exibe informações detalhadas do produto encontrado
- Interface intuitiva com feedback visual

### 2. Registro de Lotes
- Registro de lotes com informações de:
  - Código do lote
  - Mês e ano de validade
  - Quantidade disponível
- **Controle de duplicação**: Se o mesmo lote for registrado novamente, o sistema soma as quantidades automaticamente
- Formulário com validação de dados

### 3. Visualização de Lotes
- Tabela com todos os lotes registrados para cada produto
- Exibição de:
  - Código do lote
  - Data de validade (mês/ano)
  - Quantidade
  - Data de cadastro
- Total consolidado por produto

### 4. Relatórios
- **Relatório PDF**: Documento formatado com todos os produtos e lotes
- **Relatório Excel**: Planilha com dados estruturados para análise
- **Resumo do Estoque**: Estatísticas gerais incluindo:
  - Total de produtos cadastrados
  - Produtos com estoque
  - Produtos sem estoque
  - Quantidade total em estoque

### 5. Características Especiais
- **Produtos zerados incluídos**: Os relatórios mostram todos os produtos, mesmo aqueles sem estoque
- **Interface responsiva**: Funciona em desktop e dispositivos móveis
- **Design moderno**: Interface limpa e profissional
- **Feedback em tempo real**: Atualizações automáticas após cada operação

## Dados Iniciais
O sistema foi inicializado com 116 produtos do arquivo Excel fornecido, incluindo perfumes e produtos de beleza da marca Paris Elysees.

## Tecnologias Utilizadas
- **Backend**: Python Flask com SQLite
- **Frontend**: React com Tailwind CSS e shadcn/ui
- **Relatórios**: ReportLab (PDF) e pandas/openpyxl (Excel)
- **Banco de Dados**: SQLite para simplicidade e portabilidade

## Como Usar

1. **Buscar Produto**: Digite o código do produto no campo de busca e clique no botão de pesquisa
2. **Registrar Lote**: Após encontrar o produto, preencha os dados do lote (código, validade, quantidade) e clique em "Registrar Lote"
3. **Visualizar Lotes**: Os lotes registrados aparecem automaticamente na tabela à direita
4. **Gerar Relatórios**: Use os botões na seção de relatórios para baixar PDF ou Excel com todos os dados

## Estrutura do Projeto
```
estoque_app/
├── src/
│   ├── models/          # Modelos de dados (Produto, Lote)
│   ├── routes/          # APIs REST (produtos, contagem, relatórios)
│   ├── static/          # Frontend React compilado
│   └── main.py          # Aplicação principal Flask
├── venv/                # Ambiente virtual Python
└── requirements.txt     # Dependências do projeto
```

## Instalação e Execução

### Pré-requisitos
- Python 3.11+
- Node.js 20+ (para desenvolvimento do frontend)

### Executar o Sistema
1. Navegue até o diretório do projeto:
   ```bash
   cd estoque_app
   ```

2. Ative o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```

3. Execute o servidor:
   ```bash
   python src/main.py
   ```

4. Acesse no navegador: `http://localhost:5000`

## APIs Disponíveis

### Produtos
- `GET /api/produtos` - Lista todos os produtos
- `GET /api/produtos/{codigo}` - Busca produto específico

### Contagem
- `POST /api/contagem` - Registra novo lote ou atualiza existente
- `GET /api/contagem/lotes/{codigo}` - Lista lotes de um produto

### Relatórios
- `GET /api/relatorio/pdf` - Gera relatório PDF
- `GET /api/relatorio/excel` - Gera relatório Excel
- `GET /api/relatorio/resumo` - Retorna resumo do estoque

## Observações Importantes
- O sistema evita duplicação de lotes automaticamente
- Todos os produtos aparecem nos relatórios, mesmo com quantidade zero
- Os dados são persistidos em banco SQLite local
- Interface otimizada para uso em tablets e smartphones

