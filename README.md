# Sistema de Controle de Estoque

Um sistema web completo para controle de estoque com funcionalidades de cadastro de produtos, registro de contagens por lotes, geração de relatórios e integração com banco de dados PostgreSQL.

## 🚀 Funcionalidades

### 1. Cadastro/Busca de Produto
- **Busca por código**: Digite o código do produto e o sistema retorna automaticamente o nome
- **Lista de produtos**: Visualização de todos os produtos cadastrados
- **Cadastro individual**: Adicione produtos um por vez
- **Importação em lote**: Importe múltiplos produtos via planilha Excel

### 2. Registro de Estoque
Para cada produto encontrado:
- **Lote**: Identificação única do lote (não pode repetir para o mesmo produto)
- **Validade**: Mês e ano numérico da validade
- **Quantidade**: Quantidade em estoque
- **Atualização automática**: Se o mesmo produto + mesmo lote for digitado novamente, soma a quantidade

### 3. Relatórios
Geração de relatórios em PDF ou Excel (.xlsx) contendo:
- Código do produto
- Nome do produto
- Lote
- Validade
- Quantidade
- Soma das quantidades por produto
- Total geral de todas as quantidades

### 4. Interface Web Responsiva
- Design moderno e intuitivo
- Compatível com desktop e mobile
- Navegação por abas
- Feedback visual para todas as ações

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados principal
- **Flask-CORS** - Suporte a CORS
- **ReportLab** - Geração de PDFs
- **OpenPyXL** - Manipulação de arquivos Excel
- **Pandas** - Processamento de dados

### Frontend
- **HTML5** - Estrutura
- **CSS3** - Estilização responsiva
- **JavaScript (ES6+)** - Interatividade
- **Font Awesome** - Ícones

### Banco de Dados
- **PostgreSQL** - Produção (Render.com)
- **SQLite** - Desenvolvimento local

## 📋 Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git
- Conta no GitHub
- Conta no Render.com (para deploy)

## 🔧 Instalação Local

### 1. Clone o repositório
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd estoque_api
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv

# No Windows
venv\Scripts\activate

# No Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DATABASE_URL=sqlite:///estoque.db
FLASK_ENV=development
FLASK_DEBUG=True
```

### 5. Execute o aplicativo
```bash
python src/main.py
```

O aplicativo estará disponível em `http://localhost:5000`

## 📊 Estrutura do Projeto

```
estoque_api/
├── src/
│   ├── main.py                 # Aplicação principal Flask
│   ├── models/
│   │   ├── produto.py          # Modelo de Produto
│   │   └── contagem.py         # Modelo de Contagem
│   ├── routes/
│   │   ├── produto.py          # Rotas de produtos
│   │   ├── contagem.py         # Rotas de contagem
│   │   ├── relatorio.py        # Rotas de relatórios
│   │   └── importacao.py       # Rotas de importação
│   └── static/
│       ├── index.html          # Interface principal
│       ├── styles.css          # Estilos CSS
│       └── script.js           # JavaScript
├── requirements.txt            # Dependências Python
├── README.md                   # Documentação
└── .gitignore                  # Arquivos ignorados pelo Git
```

## 🗄️ Estrutura do Banco de Dados

### Tabela: produtos
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| codigo | VARCHAR(50) | Código único do produto |
| nome | VARCHAR(200) | Nome do produto |

### Tabela: contagens
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| produto_id | INTEGER | Chave estrangeira para produtos |
| lote | VARCHAR(50) | Identificação do lote |
| validade_mes | INTEGER | Mês de validade (1-12) |
| validade_ano | INTEGER | Ano de validade |
| quantidade | INTEGER | Quantidade em estoque |

## 🌐 API Endpoints

### Produtos
- `GET /api/produtos` - Lista todos os produtos
- `POST /api/produtos` - Cadastra novo produto
- `GET /api/produtos/{codigo}` - Busca produto por código
- `DELETE /api/produtos/{id}` - Remove produto

### Contagens
- `GET /api/contagens` - Lista todas as contagens
- `POST /api/contagens` - Registra nova contagem
- `DELETE /api/contagens/{id}` - Remove contagem

### Relatórios
- `GET /api/relatorio/resumo` - Resumo do estoque
- `GET /api/relatorio/pdf` - Gera relatório PDF
- `GET /api/relatorio/excel` - Gera relatório Excel

### Importação
- `GET /api/template/produtos` - Download template Excel
- `POST /api/importar/produtos` - Importa produtos via Excel

## 📱 Exemplo de Uso

### 1. Cadastrar Produto
1. Acesse a aba "Produtos"
2. Digite o código: `PROD001`
3. Digite o nome: `Arroz Tipo 1`
4. Clique em "Salvar Produto"

### 2. Registrar Contagem
1. Acesse a aba "Contagem"
2. Digite o código: `PROD001`
3. Clique em "Buscar"
4. Preencha:
   - Lote: `001`
   - Validade: `Agosto/2025`
   - Quantidade: `50`
5. Clique em "Registrar Contagem"

### 3. Gerar Relatório
1. Acesse a aba "Relatórios"
2. Clique em "Gerar PDF" ou "Gerar Excel"
3. O arquivo será baixado automaticamente

## 🔒 Segurança

- Validação de dados no frontend e backend
- Sanitização de entradas
- Tratamento de erros
- CORS configurado adequadamente
- Variáveis de ambiente para configurações sensíveis

## 🐛 Solução de Problemas

### Erro de conexão com banco de dados
- Verifique se a variável `DATABASE_URL` está configurada corretamente
- Para PostgreSQL, certifique-se de que o servidor está rodando

### Erro de dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro de CORS
- Verifique se o Flask-CORS está instalado
- Confirme a configuração no arquivo `main.py`

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👥 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte, abra uma issue no GitHub ou entre em contato através do e-mail.

