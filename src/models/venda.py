from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Usar a instância global do db
from . import db

class Venda(db.Model):
    __tablename__ = 'vendas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_venda = db.Column(db.String(20), unique=True, nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Float, nullable=False, default=0.0)
    desconto = db.Column(db.Float, default=0.0)
    valor_final = db.Column(db.Float, nullable=False, default=0.0)
    forma_pagamento = db.Column(db.String(50), nullable=False)  # Dinheiro, Cartão, PIX, etc.
    status = db.Column(db.String(20), default='Finalizada')  # Finalizada, Cancelada, Pendente
    observacoes = db.Column(db.Text, nullable=True)
    
    # Chaves estrangeiras
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    
    # Relacionamentos
    itens = db.relationship('ItemVenda', backref='venda', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Venda {self.numero_venda}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero_venda': self.numero_venda,
            'data_venda': self.data_venda.isoformat() if self.data_venda else None,
            'valor_total': self.valor_total,
            'desconto': self.desconto,
            'valor_final': self.valor_final,
            'forma_pagamento': self.forma_pagamento,
            'status': self.status,
            'observacoes': self.observacoes,
            'cliente_id': self.cliente_id,
            'funcionario_id': self.funcionario_id
        }

class ItemVenda(db.Model):
    __tablename__ = 'itens_venda'
    
    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Float, nullable=False, default=1.0)
    preco_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    tipo_item = db.Column(db.String(20), nullable=False)  # 'produto' ou 'servico'
    
    # Chaves estrangeiras
    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=True)
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=True)
    
    def __repr__(self):
        return f'<ItemVenda {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.subtotal,
            'tipo_item': self.tipo_item,
            'venda_id': self.venda_id,
            'produto_id': self.produto_id,
            'servico_id': self.servico_id
        }

