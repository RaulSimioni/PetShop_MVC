from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Usar a instância global do db
from . import db

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(50), nullable=False)  # Ração, Brinquedo, Medicamento, etc.
    marca = db.Column(db.String(80), nullable=True)
    codigo_barras = db.Column(db.String(50), unique=True, nullable=True)
    preco_custo = db.Column(db.Float, nullable=False)
    preco_venda = db.Column(db.Float, nullable=False)
    estoque_atual = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=0)
    unidade_medida = db.Column(db.String(20), default='UN')  # UN, KG, L, etc.
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    itens_venda = db.relationship('ItemVenda', backref='produto', lazy=True)
    
    def __repr__(self):
        return f'<Produto {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'marca': self.marca,
            'codigo_barras': self.codigo_barras,
            'preco_custo': self.preco_custo,
            'preco_venda': self.preco_venda,
            'estoque_atual': self.estoque_atual,
            'estoque_minimo': self.estoque_minimo,
            'unidade_medida': self.unidade_medida,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'ativo': self.ativo
        }

