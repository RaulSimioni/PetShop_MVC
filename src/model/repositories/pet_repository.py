from src.model.models import db, Pet

class PetRepository:
    def get_all(self):
        return Pet.query.all()

    def get_by_id(self, pet_id):
        return Pet.query.get(pet_id)

    def get_by_cliente_id(self, cliente_id):
        return Pet.query.filter_by(cliente_id=cliente_id).all()

    def get_active_by_cliente_id(self, cliente_id):
        return Pet.query.filter_by(cliente_id=cliente_id, ativo=True).all()

    def get_by_nome_and_cliente(self, nome, cliente_id):
        return Pet.query.filter_by(nome=nome, cliente_id=cliente_id).first()

    def add(self, pet):
        db.session.add(pet)
        db.session.commit()

    def update(self, pet):
        db.session.commit()

    def delete(self, pet):
        db.session.delete(pet)
        db.session.commit()