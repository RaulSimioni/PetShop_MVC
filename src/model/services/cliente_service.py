from src.model.repositories.cliente_repository import ClienteRepository
from src.model.models import Cliente

class ClienteService:
    def __init__(self):
        self.cliente_repository = ClienteRepository()

    def get_all_clientes(self):
        return self.cliente_repository.get_all()

    def get_cliente_by_id(self, cliente_id):
        return self.cliente_repository.get_by_id(cliente_id)

    def get_cliente_by_cpf(self, cpf):
        return self.cliente_repository.get_by_cpf(cpf)

    def get_cliente_by_email(self, email):
        return self.cliente_repository.get_by_email(email)

    def create_cliente(self, nome, cpf, telefone, email, endereco):
        if not nome or not cpf or not telefone:
            raise ValueError("Nome, CPF e telefone são obrigatórios")

        if self.cliente_repository.get_by_cpf(cpf):
            raise ValueError("CPF já cadastrado")

        if email and self.cliente_repository.get_by_email(email):
            raise ValueError("Email já cadastrado")

        new_cliente = Cliente(nome=nome, cpf=cpf, telefone=telefone, email=email, endereco=endereco)
        self.cliente_repository.add(new_cliente)
        return new_cliente

    def update_cliente(self, cliente_id, nome, cpf, telefone, email, endereco, ativo):
        cliente = self.cliente_repository.get_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado")

        if not nome or not cpf or not telefone:
            raise ValueError("Nome, CPF e telefone são obrigatórios")

        cpf_existente = self.cliente_repository.get_by_cpf(cpf)
        if cpf_existente and cpf_existente.id != cliente_id:
            raise ValueError("CPF já cadastrado para outro cliente")

        if email:
            email_existente = self.cliente_repository.get_by_email(email)
            if email_existente and email_existente.id != cliente_id:
                raise ValueError("Email já cadastrado para outro cliente")

        cliente.nome = nome if nome is not None else cliente.nome
        cliente.cpf = cpf if cpf is not None else cliente.cpf
        cliente.telefone = telefone if telefone is not None else cliente.telefone
        cliente.email = email if email is not None else cliente.email
        cliente.endereco = endereco if endereco is not None else cliente.endereco
        cliente.ativo = ativo if ativo is not None else cliente.ativo
        self.cliente_repository.update(cliente)
        return cliente

    def deactivate_cliente(self, cliente_id):
        cliente = self.cliente_repository.get_by_id(cliente_id)
        if cliente:
            cliente.ativo = False
            self.cliente_repository.update(cliente)
            return True
        return False

    def activate_cliente(self, cliente_id):
        cliente = self.cliente_repository.get_by_id(cliente_id)
        if cliente:
            cliente.ativo = True
            self.cliente_repository.update(cliente)
            return cliente
        return None

    def get_pets_by_cliente_id(self, cliente_id):
        cliente = self.cliente_repository.get_by_id(cliente_id)
        if cliente:
            return [pet for pet in cliente.pets if pet.ativo]
        return None


