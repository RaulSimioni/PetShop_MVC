from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Usar a instância global do db
from . import db

class Pet(db.Model):
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    especie = db.Column(db.String(50), nullable=False)  # Cão, Gato, etc.
    raca = db.Column(db.String(80), nullable=True)
    cor = db.Column(db.String(50), nullable=True)
    sexo = db.Column(db.String(10), nullable=False)  # Macho, Fêmea
    data_nascimento = db.Column(db.Date, nullable=True)
    peso = db.Column(db.Float, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    # Chave estrangeira
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    
    # Relacionamentos
    agendamentos = db.relationship('Agendamento', backref='pet', lazy=True)
    
    @property
    def idade(self):
        """Calcula a idade do pet em anos"""
        if self.data_nascimento:
            from datetime import date
            hoje = date.today()
            idade_dias = (hoje - self.data_nascimento).days
            return round(idade_dias / 365.25, 1)
        return None
    
    def __repr__(self):
        return f'<Pet {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'especie': self.especie,
            'raca': self.raca,
            'cor': self.cor,
            'sexo': self.sexo,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'peso': self.peso,
            'observacoes': self.observacoes,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'ativo': self.ativo,
            'cliente_id': self.cliente_id
        }

