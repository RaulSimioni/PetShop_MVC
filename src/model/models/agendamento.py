from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Usar a instância global do db
from . import db

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    data_agendamento = db.Column(db.DateTime, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Agendado')  # Agendado, Confirmado, Em Andamento, Concluído, Cancelado
    observacoes = db.Column(db.Text, nullable=True)
    valor_estimado = db.Column(db.Float, nullable=True)
    tempo_estimado = db.Column(db.Integer, nullable=True)  # em minutos
    
    # Chaves estrangeiras
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)  # Pet agora é obrigatório
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    
    def __repr__(self):
        return f'<Agendamento {self.id} - {self.data_agendamento}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'data_agendamento': self.data_agendamento.isoformat() if self.data_agendamento else None,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'status': self.status,
            'observacoes': self.observacoes,
            'valor_estimado': self.valor_estimado,
            'tempo_estimado': self.tempo_estimado,
            'cliente_id': self.cliente_id,
            'pet_id': self.pet_id,
            'servico_id': self.servico_id,
            'funcionario_id': self.funcionario_id
        }

