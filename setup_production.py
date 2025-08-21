import os
import sys
import pandas as pd

# Adiciona a pasta src ao path para importar o main.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import app, db
from src.models.produto import Produto


# Caminho do arquivo Excel
EXCEL_PATH = os.path.join(os.path.dirname(__file__), 'produtos.xlsx')

with app.app_context():
    db.create_all()

    # Lê o arquivo Excel (sem cabeçalho)
    df = pd.read_excel(EXCEL_PATH, header=None)

    for _, row in df.iterrows():
        codigo = str(row[0]).strip()
        nome = str(row[1]).strip()

        if not Produto.query.filter_by(codigo=codigo).first():
            db.session.add(Produto(
                codigo=codigo,
                nome=nome
            ))

    db.session.commit()

print("✅ Importação concluída com sucesso!")
