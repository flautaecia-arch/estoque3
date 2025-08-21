# Guia de Deployment - Sistema de Contagem de Estoque

## 📋 Pré-requisitos
- Conta no GitHub
- Conta no Render.com

## 🚀 Deploy no Render

### Passo 1: Preparar o Repositório GitHub
1. Crie um novo repositório no GitHub
2. Faça upload de todos os arquivos do projeto para o repositório
3. Certifique-se de que os seguintes arquivos estão incluídos:
   - `render.yaml` (configuração do Render)
   - `requirements.txt` (dependências Python)
   - `setup_production.py` (script de inicialização)
   - Todo o código fonte na pasta `src/`

### Passo 2: Deploy no Render
1. Acesse [render.com](https://render.com) e faça login
2. Clique em "New +" → "Web Service"
3. Conecte seu repositório GitHub
4. Selecione o repositório do projeto
5. Configure as seguintes opções:
   - **Name**: `sistema-contagem-estoque`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python setup_production.py`
   - **Start Command**: `python src/main.py`
6. Clique em "Create Web Service"

### Passo 3: Configuração Automática
O Render detectará automaticamente o arquivo `render.yaml` e aplicará as configurações:
- Python 3.11
- Disco persistente para o banco SQLite
- Variáveis de ambiente necessárias
- Health check configurado

## 🔧 Configurações Importantes

### Variáveis de Ambiente
O sistema está configurado para usar:
- `PORT`: Porta fornecida pelo Render (automática)
- `PYTHON_VERSION`: 3.11.0

### Banco de Dados
- SQLite com disco persistente
- Inicialização automática dos 116 produtos
- Dados persistem entre deployments

### Arquivos Principais
- `src/main.py`: Aplicação Flask principal
- `setup_production.py`: Script de inicialização para produção
- `render.yaml`: Configuração do Render
- `requirements.txt`: Dependências Python

## 📁 Estrutura para GitHub

```
sistema-contagem-estoque/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── produto.py
│   │   └── lote.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── produto.py
│   │   ├── contagem.py
│   │   └── relatorio.py
│   ├── static/
│   │   ├── index.html
│   │   ├── assets/
│   │   └── ...
│   ├── database/
│   │   └── (será criado automaticamente)
│   └── main.py
├── render.yaml
├── requirements.txt
├── setup_production.py
├── README.md
├── DEPLOYMENT.md
├── .gitignore
└── LICENSE (opcional)
```

## 🎯 Após o Deploy

1. O Render fornecerá uma URL pública (ex: `https://sistema-contagem-estoque.onrender.com`)
2. O sistema estará disponível 24/7
3. SSL/HTTPS automático
4. Backup automático do banco de dados

## 🔍 Verificação

Após o deploy, teste:
1. Acesso à página principal
2. Busca de produtos
3. Registro de lotes
4. Geração de relatórios PDF/Excel
5. Funcionalidade de soma de lotes duplicados

## 🆘 Troubleshooting

### Build Falha
- Verifique se `requirements.txt` está correto
- Confirme que `setup_production.py` está no diretório raiz

### Aplicação não Inicia
- Verifique logs no dashboard do Render
- Confirme que `src/main.py` existe e está correto

### Banco de Dados Vazio
- Verifique se `setup_production.py` foi executado no build
- Confirme que o disco persistente está configurado

## 📞 Suporte

Em caso de problemas:
1. Verifique os logs no dashboard do Render
2. Confirme que todos os arquivos foram enviados para o GitHub
3. Teste localmente antes do deploy

