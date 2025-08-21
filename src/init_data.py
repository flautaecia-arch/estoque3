import pandas as pd
import sys
import os

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import app
from src.models.produto import Produto
from src.models.user import db

def init_produtos():
    """Inicializa a base de dados com os produtos do arquivo Excel"""
    
    # Caminho para o arquivo Excel
    excel_file = '/home/ubuntu/upload/produtos(1).xlsx'
    
    try:
        # Ler o arquivo Excel
        df = pd.read_excel(excel_file)
        
        with app.app_context():
            # Limpar produtos existentes (opcional)
            Produto.query.delete()
            
            # Inserir produtos do Excel
            for _, row in df.iterrows():
                # As colunas são a primeira e segunda do DataFrame
                codigo = str(row.iloc[0])  # Primeira coluna
                nome = str(row.iloc[1])    # Segunda coluna
                
                produto = Produto(
                    codigo=codigo,
                    nome=nome
                )
                db.session.add(produto)
            
            # Salvar mudanças
            db.session.commit()
            print(f"Produtos inicializados com sucesso! Total: {len(df)} produtos.")
            
    except Exception as e:
        print(f"Erro ao inicializar produtos: {str(e)}")

if __name__ == '__main__':
    init_produtos()

