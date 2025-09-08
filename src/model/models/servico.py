from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Usar a instância global do db
from . import db

class Servico(db.Model):
    __tablename__ = 'servicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(50), nullable=False)  # Banho, Tosa, Consulta, etc.
    preco = db.Column(db.Float, nullable=False)
    duracao_estimada = db.Column(db.Integer, nullable=True)  # em minutos
    observacoes = db.Column(db.Text, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    agendamentos = db.relationship('Agendamento', backref='servico', lazy=True)
    itens_venda = db.relationship('ItemVenda', backref='servico', lazy=True)
    
    def __repr__(self):
        return f'<Servico {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'preco': self.preco,
            'duracao_estimada': self.duracao_estimada,
            'observacoes': self.observacoes,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'ativo': self.ativo
        }

