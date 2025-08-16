import os
import sys
import tempfile

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.produto import produto_bp
from src.routes.contagem import contagem_bp
from src.routes.relatorio import relatorio_bp
from src.routes.importacao import importacao_bp

from src.models.produto import Produto
from src.models.contagem import Contagem

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS para todas as rotas
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(produto_bp, url_prefix='/api')
app.register_blueprint(contagem_bp, url_prefix='/api')
app.register_blueprint(relatorio_bp, url_prefix='/api')
app.register_blueprint(importacao_bp, url_prefix='/api')

# Configuração do banco de dados (usando /tmp no Render)
temp_db = os.path.join(tempfile.gettempdir(), "app.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{temp_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Carregar produtos iniciais do JSON
import json

with app.app_context():
    db.create_all()

    # Carregar produtos iniciais do JSON, apenas se o banco estiver vazio
    if Produto.query.count() == 0:
        produtos_path = os.path.join(os.path.dirname(__file__), "produtos.json")
        if os.path.exists(produtos_path):
            with open(produtos_path, "r", encoding="utf-8") as f:
                produtos = json.load(f)
                for p in produtos:
                    novo_produto = Produto(
                        codigo=p["codigo"],
                        nome=p["nome"],
                        preco=p.get("preco", 0.0),
                        unidade=p.get("unidade", "UN"),
                        quantidade=p.get("quantidade", 0)
                    )
                    db.session.add(novo_produto)
                db.session.commit()
                print("✅ Produtos iniciais carregados no banco!")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
