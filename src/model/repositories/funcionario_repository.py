from src.model.models import db, Funcionario

class FuncionarioRepository:
    def get_all(self):
        return Funcionario.query.all()

    def get_by_id(self, funcionario_id):
        return Funcionario.query.get(funcionario_id)

    def get_by_cpf(self, cpf):
        return Funcionario.query.filter_by(cpf=cpf).first()

    def get_by_email(self, email):
        return Funcionario.query.filter_by(email=email).first()

    def add(self, funcionario):
        db.session.add(funcionario)
        db.session.commit()

    def update(self, funcionario):
        db.session.commit()

    def delete(self, funcionario):
        db.session.delete(funcionario)
        db.session.commit()