from src.models.user import db
from datetime import datetime

class Lote(db.Model):
    __tablename__ = 'lotes'
    
    id = db.Column(db.Integer, primary_key=True)
    produto_codigo = db.Column(db.String(20), db.ForeignKey('produtos.codigo'), nullable=False)
    lote = db.Column(db.String(50), nullable=False)
    validade_mes = db.Column(db.Integer, nullable=False)
    validade_ano = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índice único para evitar duplicação de lotes por produto
    __table_args__ = (db.UniqueConstraint('produto_codigo', 'lote', name='unique_produto_lote'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'produto_codigo': self.produto_codigo,
            'lote': self.lote,
            'validade_mes': self.validade_mes,
            'validade_ano': self.validade_ano,
            'quantidade': self.quantidade,
            'data_cadastro': self.data_cadastro.strftime('%d/%m/%Y')
        }

