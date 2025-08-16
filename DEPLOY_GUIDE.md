# 🚀 Guia de Deploy - GitHub + Render.com

Este guia fornece instruções detalhadas para fazer o deploy do Sistema de Controle de Estoque no GitHub e Render.com.

## 📋 Pré-requisitos

- [ ] Conta no GitHub
- [ ] Conta no Render.com
- [ ] Git instalado localmente
- [ ] Projeto funcionando localmente

## 🔧 Parte 1: Preparação do Projeto

### 1.1 Configurar variáveis de ambiente para produção

Edite o arquivo `src/main.py` e certifique-se de que está configurado para produção:

```python
import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.produto import Produto, Base
from models.contagem import Contagem
from routes.produto import produto_bp
from routes.contagem import contagem_bp
from routes.relatorio import relatorio_bp
from routes.importacao import importacao_bp

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Configuração do banco de dados
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///estoque.db')

# Fix para Render.com PostgreSQL URL
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Criar tabelas
Base.metadata.create_all(engine)

# Registrar blueprints
app.register_blueprint(produto_bp, url_prefix='/api')
app.register_blueprint(contagem_bp, url_prefix='/api')
app.register_blueprint(relatorio_bp, url_prefix='/api')
app.register_blueprint(importacao_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### 1.2 Atualizar requirements.txt

Certifique-se de que o arquivo `requirements.txt` contém todas as dependências:

```txt
Flask==3.1.1
Flask-CORS==6.0.0
SQLAlchemy==2.0.36
psycopg2-binary==2.9.10
pandas==2.3.1
openpyxl==3.1.5
reportlab==4.4.3
Werkzeug==3.1.3
```

### 1.3 Criar arquivo .gitignore

Crie um arquivo `.gitignore` na raiz do projeto:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# Environment Variables
.env
.env.local
.env.production

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
temp/
tmp/
```

### 1.4 Mover arquivos HTML para templates

Crie a estrutura de templates do Flask:

```bash
mkdir -p src/templates
mv src/static/index.html src/templates/
```

Atualize o arquivo `src/main.py` para usar templates:

```python
app = Flask(__name__, 
           static_folder='static', 
           static_url_path='',
           template_folder='templates')
```

## 🐙 Parte 2: Deploy no GitHub

### 2.1 Inicializar repositório Git

```bash
# Na raiz do projeto estoque_api
git init
git add .
git commit -m "Initial commit: Sistema de Controle de Estoque"
```

### 2.2 Criar repositório no GitHub

1. Acesse [GitHub.com](https://github.com)
2. Clique em "New repository"
3. Nome do repositório: `sistema-controle-estoque`
4. Descrição: `Sistema web para controle de estoque com Flask e PostgreSQL`
5. Marque como **Público** ou **Privado** (sua escolha)
6. **NÃO** marque "Add a README file" (já temos um)
7. Clique em "Create repository"

### 2.3 Conectar repositório local ao GitHub

```bash
# Substitua SEU_USUARIO pelo seu nome de usuário do GitHub
git remote add origin https://github.com/SEU_USUARIO/sistema-controle-estoque.git
git branch -M main
git push -u origin main
```

### 2.4 Verificar upload

1. Acesse seu repositório no GitHub
2. Verifique se todos os arquivos foram enviados
3. Confirme se o README.md está sendo exibido

## ☁️ Parte 3: Deploy no Render.com

### 3.1 Criar conta no Render.com

1. Acesse [Render.com](https://render.com)
2. Clique em "Get Started for Free"
3. Faça login com sua conta GitHub
4. Autorize o Render a acessar seus repositórios

### 3.2 Criar banco de dados PostgreSQL

1. No dashboard do Render, clique em "New +"
2. Selecione "PostgreSQL"
3. Configurações:
   - **Name**: `estoque-database`
   - **Database**: `estoque_db`
   - **User**: `estoque_user`
   - **Region**: `Oregon (US West)` (ou mais próximo)
   - **PostgreSQL Version**: `16`
   - **Plan**: `Free` (para teste)
4. Clique em "Create Database"
5. **IMPORTANTE**: Copie a "External Database URL" - você precisará dela

### 3.3 Criar Web Service

1. No dashboard do Render, clique em "New +"
2. Selecione "Web Service"
3. Conecte seu repositório GitHub:
   - Clique em "Connect account" se necessário
   - Selecione o repositório `sistema-controle-estoque`
   - Clique em "Connect"

### 3.4 Configurar Web Service

**Configurações básicas:**
- **Name**: `sistema-controle-estoque`
- **Region**: `Oregon (US West)` (mesmo do banco)
- **Branch**: `main`
- **Root Directory**: deixe vazio
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python src/main.py`

**Configurações avançadas:**
- **Plan**: `Free` (para teste)
- **Python Version**: `3.11.0`

### 3.5 Configurar variáveis de ambiente

Na seção "Environment Variables", adicione:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Cole a "External Database URL" do PostgreSQL |
| `FLASK_ENV` | `production` |
| `PORT` | `10000` |

### 3.6 Deploy

1. Clique em "Create Web Service"
2. O Render iniciará o processo de build e deploy
3. Acompanhe os logs na aba "Logs"
4. O processo pode levar 5-10 minutos

### 3.7 Verificar deploy

1. Quando o status mostrar "Live", clique na URL do serviço
2. Teste todas as funcionalidades:
   - Cadastro de produto
   - Busca de produto
   - Registro de contagem
   - Geração de relatórios

## 🔧 Parte 4: Configurações Adicionais

### 4.1 Domínio customizado (Opcional)

Se você tem um domínio próprio:

1. Na página do seu Web Service no Render
2. Vá para "Settings" > "Custom Domains"
3. Clique em "Add Custom Domain"
4. Digite seu domínio
5. Configure os registros DNS conforme instruído

### 4.2 Monitoramento

O Render oferece monitoramento básico gratuito:
- Logs em tempo real
- Métricas de CPU e memória
- Alertas por email

### 4.3 Backup do banco de dados

Para fazer backup do PostgreSQL:

1. Acesse o dashboard do banco no Render
2. Vá para "Info" > "Connections"
3. Use as credenciais para conectar via `pg_dump`:

```bash
pg_dump -h <hostname> -U <username> -d <database> > backup.sql
```

## 🚨 Solução de Problemas

### Erro de build no Render

**Problema**: Falha na instalação de dependências
**Solução**: 
1. Verifique se o `requirements.txt` está correto
2. Confirme se está na raiz do projeto
3. Teste localmente: `pip install -r requirements.txt`

### Erro de conexão com banco

**Problema**: Aplicação não conecta ao PostgreSQL
**Solução**:
1. Verifique se a `DATABASE_URL` está correta
2. Confirme se o banco está "Available"
3. Teste a conexão nas configurações do banco

### Aplicação não carrega

**Problema**: Erro 503 ou timeout
**Solução**:
1. Verifique os logs na aba "Logs"
2. Confirme se o comando de start está correto
3. Teste se a aplicação roda na porta correta

### Arquivos estáticos não carregam

**Problema**: CSS/JS não funcionam
**Solução**:
1. Verifique se os arquivos estão em `src/static/`
2. Confirme a configuração do Flask para arquivos estáticos
3. Teste localmente primeiro

## 📊 Monitoramento e Manutenção

### Logs

Para acessar logs em tempo real:
1. Acesse seu Web Service no Render
2. Clique na aba "Logs"
3. Use os filtros para encontrar erros específicos

### Atualizações

Para atualizar o aplicativo:

1. Faça as alterações localmente
2. Commit e push para o GitHub:
```bash
git add .
git commit -m "Descrição da atualização"
git push origin main
```
3. O Render fará o redeploy automaticamente

### Escalabilidade

Para aumentar a capacidade:
1. Upgrade para um plano pago no Render
2. Configure auto-scaling se necessário
3. Considere usar Redis para cache

## 🎯 URLs Finais

Após o deploy bem-sucedido, você terá:

- **Aplicação**: `https://sistema-controle-estoque.onrender.com`
- **Banco de dados**: Gerenciado pelo Render
- **Repositório**: `https://github.com/SEU_USUARIO/sistema-controle-estoque`

## ✅ Checklist Final

- [ ] Código commitado no GitHub
- [ ] Banco PostgreSQL criado no Render
- [ ] Web Service configurado no Render
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado com sucesso
- [ ] Aplicação testada em produção
- [ ] Backup do banco configurado (opcional)
- [ ] Domínio customizado configurado (opcional)

## 📞 Suporte

Se encontrar problemas:

1. **Render Support**: [help.render.com](https://help.render.com)
2. **GitHub Issues**: Crie uma issue no seu repositório
3. **Documentação Flask**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
4. **Documentação PostgreSQL**: [postgresql.org/docs](https://www.postgresql.org/docs/)

---

**Parabéns! 🎉** Seu Sistema de Controle de Estoque está agora rodando na nuvem e acessível para qualquer pessoa com a URL!

