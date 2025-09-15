from src.model.repositories.pet_repository import PetRepository
from src.model.repositories.cliente_repository import ClienteRepository
from src.model.models import Pet
from datetime import datetime

class PetService:
    def __init__(self):
        self.pet_repository = PetRepository()
        self.cliente_repository = ClienteRepository()

    def get_all_pets(self):
        return self.pet_repository.get_all()

    def get_pet_by_id(self, pet_id):
        return self.pet_repository.get_by_id(pet_id)

    def get_pets_by_cliente_id(self, cliente_id):
        return self.pet_repository.get_by_cliente_id(cliente_id)

    def get_active_pets_by_cliente_id(self, cliente_id):
        return self.pet_repository.get_active_by_cliente_id(cliente_id)

    def create_pet(self, nome, especie, cliente_id, raca=None, cor=None, sexo=None, data_nascimento=None, peso=None, observacoes=None):
        # Validações obrigatórias
        if not nome or not especie or not cliente_id:
            raise ValueError("Nome, espécie e cliente são obrigatórios")

        # Verificar se o cliente existe
        cliente = self.cliente_repository.get_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado")

        if not cliente.ativo:
            raise ValueError("Não é possível cadastrar pet para cliente inativo")

        # Verificar se já existe um pet com o mesmo nome para o mesmo cliente
        pet_existente = self.pet_repository.get_by_nome_and_cliente(nome, cliente_id)
        if pet_existente:
            raise ValueError("Já existe um pet com este nome para este cliente")

        # Validações específicas
        especies_validas = ["Cão", "Gato", "Pássaro", "Peixe", "Hamster", "Coelho", "Réptil", "Outros"]
        if especie not in especies_validas:
            raise ValueError(f"Espécie deve ser uma das seguintes: {', '.join(especies_validas)}")

        if sexo and sexo not in ["Macho", "Fêmea"]:
            raise ValueError("Sexo deve ser 'Macho' ou 'Fêmea'")

        if peso is not None and peso <= 0:
            raise ValueError("Peso deve ser maior que zero")

        # Validar data de nascimento
        if data_nascimento and data_nascimento > datetime.now().date():
            raise ValueError("Data de nascimento não pode ser no futuro")

        new_pet = Pet(
            nome=nome,
            especie=especie,
            raca=raca,
            cor=cor,
            sexo=sexo,
            data_nascimento=data_nascimento,
            peso=peso,
            observacoes=observacoes,
            cliente_id=cliente_id
        )
        
        self.pet_repository.add(new_pet)
        return new_pet

    def update_pet(self, pet_id, nome=None, especie=None, raca=None, cor=None, sexo=None, data_nascimento=None, peso=None, observacoes=None, ativo=None, cliente_id=None):
        pet = self.pet_repository.get_by_id(pet_id)
        if not pet:
            raise ValueError("Pet não encontrado")

        # Validações obrigatórias
        if nome is not None and not nome:
            raise ValueError("Nome é obrigatório")
        
        if especie is not None and not especie:
            raise ValueError("Espécie é obrigatória")

        # Se mudando de cliente, verificar se o novo cliente existe e está ativo
        if cliente_id is not None and cliente_id != pet.cliente_id:
            cliente = self.cliente_repository.get_by_id(cliente_id)
            if not cliente:
                raise ValueError("Cliente não encontrado")
            if not cliente.ativo:
                raise ValueError("Não é possível transferir pet para cliente inativo")

        # Verificar se já existe um pet com o mesmo nome para o mesmo cliente (exceto o atual)
        if nome is not None and nome != pet.nome:
            cliente_check_id = cliente_id if cliente_id is not None else pet.cliente_id
            pet_existente = self.pet_repository.get_by_nome_and_cliente(nome, cliente_check_id)
            if pet_existente and pet_existente.id != pet_id:
                raise ValueError("Já existe um pet com este nome para este cliente")

        # Validações específicas
        if especie is not None:
            especies_validas = ["Cão", "Gato", "Pássaro", "Peixe", "Hamster", "Coelho", "Réptil", "Outros"]
            if especie not in especies_validas:
                raise ValueError(f"Espécie deve ser uma das seguintes: {', '.join(especies_validas)}")

        if sexo is not None and sexo not in ["Macho", "Fêmea"]:
            raise ValueError("Sexo deve ser 'Macho' ou 'Fêmea'")

        if peso is not None and peso <= 0:
            raise ValueError("Peso deve ser maior que zero")

        # Validar data de nascimento
        if data_nascimento is not None and data_nascimento > datetime.now().date():
            raise ValueError("Data de nascimento não pode ser no futuro")

        # Atualizar dados
        if nome is not None:
            pet.nome = nome
        if especie is not None:
            pet.especie = especie
        if raca is not None:
            pet.raca = raca
        if cor is not None:
            pet.cor = cor
        if sexo is not None:
            pet.sexo = sexo
        if data_nascimento is not None:
            pet.data_nascimento = data_nascimento
        if peso is not None:
            pet.peso = peso
        if observacoes is not None:
            pet.observacoes = observacoes
        if ativo is not None:
            pet.ativo = ativo
        if cliente_id is not None:
            pet.cliente_id = cliente_id

        self.pet_repository.update(pet)
        return pet

    def deactivate_pet(self, pet_id):
        pet = self.pet_repository.get_by_id(pet_id)
        if pet:
            pet.ativo = False
            self.pet_repository.update(pet)
            return True
        return False

    def activate_pet(self, pet_id):
        pet = self.pet_repository.get_by_id(pet_id)
        if pet:
            # Verificar se o cliente ainda está ativo
            if not pet.dono.ativo:
                raise ValueError("Não é possível ativar pet de cliente inativo")
            
            pet.ativo = True
            self.pet_repository.update(pet)
            return pet
        return None

    def get_especies_disponiveis(self):
        return ["Cão", "Gato", "Pássaro", "Peixe", "Hamster", "Coelho", "Réptil", "Outros"]

    def get_sexos_disponiveis(self):
        return ["Macho", "Fêmea"]