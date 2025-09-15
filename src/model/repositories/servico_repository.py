from src.model.models import db, Servico

class ServicoRepository:
    def get_all(self):
        return Servico.query.all()

    def get_by_id(self, servico_id):
        return Servico.query.get(servico_id)

    def get_by_nome(self, nome):
        return Servico.query.filter_by(nome=nome).first()

    def get_by_categoria(self, categoria):
        return Servico.query.filter_by(categoria=categoria).all()

    def get_active(self):
        return Servico.query.filter_by(ativo=True).all()

    def add(self, servico):
        db.session.add(servico)
        db.session.commit()

    def update(self, servico):
        db.session.commit()

    def delete(self, servico):
        db.session.delete(servico)
        db.session.commit()