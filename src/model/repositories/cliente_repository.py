from src.model.models import db, Cliente

class ClienteRepository:
    def get_all(self):
        return Cliente.query.all()

    def get_by_id(self, cliente_id):
        return Cliente.query.get(cliente_id)

    def get_by_cpf(self, cpf):
        return Cliente.query.filter_by(cpf=cpf).first()

    def get_by_email(self, email):
        return Cliente.query.filter_by(email=email).first()

    def add(self, cliente):
        db.session.add(cliente)
        db.session.commit()

    def update(self, cliente):
        db.session.commit()

    def delete(self, cliente):
        db.session.delete(cliente)
        db.session.commit()


