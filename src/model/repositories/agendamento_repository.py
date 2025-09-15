from src.model.models import db, Agendamento

class AgendamentoRepository:
    def get_all(self):
        return Agendamento.query.all()

    def get_by_id(self, agendamento_id):
        return Agendamento.query.get(agendamento_id)

    def get_by_cliente_id(self, cliente_id):
        return Agendamento.query.filter_by(cliente_id=cliente_id).all()

    def get_by_funcionario_id(self, funcionario_id):
        return Agendamento.query.filter_by(funcionario_id=funcionario_id).all()

    def get_by_servico_id(self, servico_id):
        return Agendamento.query.filter_by(servico_id=servico_id).all()

    def get_by_status(self, status):
        return Agendamento.query.filter_by(status=status).all()

    def get_by_date_range(self, data_inicio, data_fim):
        return Agendamento.query.filter(
            Agendamento.data_agendamento >= data_inicio,
            Agendamento.data_agendamento <= data_fim
        ).all()

    def add(self, agendamento):
        db.session.add(agendamento)
        db.session.commit()

    def update(self, agendamento):
        db.session.commit()

    def delete(self, agendamento):
        db.session.delete(agendamento)
        db.session.commit()