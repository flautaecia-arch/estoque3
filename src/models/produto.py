from src.models.user import db

class Produto(db.Model):
    __tablename__ = 'produtos'
    __table_args__ = {'extend_existing': True}  # <-- Evita conflito no Render
    
    codigo = db.Column(db.String(20), primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    
    def to_dict(self):
        return {
            'codigo': self.codigo,
            'nome': self.nome
        }
