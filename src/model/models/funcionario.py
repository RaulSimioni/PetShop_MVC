from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Usar a instância global do db
from . import db

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    endereco = db.Column(db.Text, nullable=True)
    cargo = db.Column(db.String(80), nullable=False)
    salario = db.Column(db.Float, nullable=True)
    data_admissao = db.Column(db.Date, nullable=False)
    data_demissao = db.Column(db.Date, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    agendamentos = db.relationship('Agendamento', backref='funcionario', lazy=True)
    
    def __repr__(self):
        return f'<Funcionario {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco,
            'cargo': self.cargo,
            'salario': self.salario,
            'data_admissao': self.data_admissao.isoformat() if self.data_admissao else None,
            'data_demissao': self.data_demissao.isoformat() if self.data_demissao else None,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'ativo': self.ativo
        }

