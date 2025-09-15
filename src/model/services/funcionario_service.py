from src.model.repositories.funcionario_repository import FuncionarioRepository
from src.model.models import Funcionario
from datetime import datetime

class FuncionarioService:
    def __init__(self):
        self.funcionario_repository = FuncionarioRepository()

    def get_all_funcionarios(self):
        return self.funcionario_repository.get_all()

    def get_funcionario_by_id(self, funcionario_id):
        return self.funcionario_repository.get_by_id(funcionario_id)

    def get_funcionario_by_cpf(self, cpf):
        return self.funcionario_repository.get_by_cpf(cpf)

    def get_funcionario_by_email(self, email):
        return self.funcionario_repository.get_by_email(email)

    def create_funcionario(self, nome, cpf, telefone, email, endereco, cargo, salario, data_admissao):
        if not nome or not cpf or not telefone or not cargo or not data_admissao:
            raise ValueError("Nome, CPF, telefone, cargo e data de admissão são obrigatórios")

        if self.funcionario_repository.get_by_cpf(cpf):
            raise ValueError("CPF já cadastrado")

        if email and self.funcionario_repository.get_by_email(email):
            raise ValueError("Email já cadastrado")

        # Converter string de data para objeto date se necessário
        if isinstance(data_admissao, str):
            try:
                data_admissao = datetime.strptime(data_admissao, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Formato de data inválido. Use YYYY-MM-DD")

        new_funcionario = Funcionario(
            nome=nome, 
            cpf=cpf, 
            telefone=telefone, 
            email=email, 
            endereco=endereco,
            cargo=cargo,
            salario=salario,
            data_admissao=data_admissao
        )
        self.funcionario_repository.add(new_funcionario)
        return new_funcionario

    def update_funcionario(self, funcionario_id, nome, cpf, telefone, email, endereco, cargo, salario, data_admissao, data_demissao, ativo):
        funcionario = self.funcionario_repository.get_by_id(funcionario_id)
        if not funcionario:
            raise ValueError("Funcionário não encontrado")

        if not nome or not cpf or not telefone or not cargo or not data_admissao:
            raise ValueError("Nome, CPF, telefone, cargo e data de admissão são obrigatórios")

        cpf_existente = self.funcionario_repository.get_by_cpf(cpf)
        if cpf_existente and cpf_existente.id != funcionario_id:
            raise ValueError("CPF já cadastrado para outro funcionário")

        if email:
            email_existente = self.funcionario_repository.get_by_email(email)
            if email_existente and email_existente.id != funcionario_id:
                raise ValueError("Email já cadastrado para outro funcionário")

        # Converter strings de data para objetos date se necessário
        if isinstance(data_admissao, str):
            try:
                data_admissao = datetime.strptime(data_admissao, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Formato de data de admissão inválido. Use YYYY-MM-DD")

        if data_demissao and isinstance(data_demissao, str):
            try:
                data_demissao = datetime.strptime(data_demissao, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Formato de data de demissão inválido. Use YYYY-MM-DD")

        funcionario.nome = nome if nome is not None else funcionario.nome
        funcionario.cpf = cpf if cpf is not None else funcionario.cpf
        funcionario.telefone = telefone if telefone is not None else funcionario.telefone
        funcionario.email = email if email is not None else funcionario.email
        funcionario.endereco = endereco if endereco is not None else funcionario.endereco
        funcionario.cargo = cargo if cargo is not None else funcionario.cargo
        funcionario.salario = salario if salario is not None else funcionario.salario
        funcionario.data_admissao = data_admissao if data_admissao is not None else funcionario.data_admissao
        funcionario.data_demissao = data_demissao if data_demissao is not None else funcionario.data_demissao
        funcionario.ativo = ativo if ativo is not None else funcionario.ativo
        
        self.funcionario_repository.update(funcionario)
        return funcionario

    def deactivate_funcionario(self, funcionario_id):
        funcionario = self.funcionario_repository.get_by_id(funcionario_id)
        if funcionario:
            funcionario.ativo = False
            funcionario.data_demissao = datetime.now().date()
            self.funcionario_repository.update(funcionario)
            return True
        return False

    def activate_funcionario(self, funcionario_id):
        funcionario = self.funcionario_repository.get_by_id(funcionario_id)
        if funcionario:
            funcionario.ativo = True
            funcionario.data_demissao = None
            self.funcionario_repository.update(funcionario)
            return funcionario
        return None

    def get_agendamentos_by_funcionario_id(self, funcionario_id):
        funcionario = self.funcionario_repository.get_by_id(funcionario_id)
        if funcionario:
            return funcionario.agendamentos
        return None