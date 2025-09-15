from src.model.repositories.servico_repository import ServicoRepository
from src.model.models import Servico

class ServicoService:
    def __init__(self):
        self.servico_repository = ServicoRepository()

    def get_all_servicos(self):
        return self.servico_repository.get_all()

    def get_servico_by_id(self, servico_id):
        return self.servico_repository.get_by_id(servico_id)

    def get_servico_by_nome(self, nome):
        return self.servico_repository.get_by_nome(nome)

    def get_servicos_by_categoria(self, categoria):
        return self.servico_repository.get_by_categoria(categoria)

    def get_active_servicos(self):
        return self.servico_repository.get_active()

    def create_servico(self, nome, categoria, preco, descricao=None, duracao_estimada=None, observacoes=None):
        if not nome or not categoria or preco is None:
            raise ValueError("Nome, categoria e preço são obrigatórios")

        if self.servico_repository.get_by_nome(nome):
            raise ValueError("Já existe um serviço com este nome")

        if preco < 0:
            raise ValueError("Preço deve ser um valor positivo")

        if duracao_estimada is not None and duracao_estimada < 0:
            raise ValueError("Duração estimada deve ser um valor positivo")

        new_servico = Servico(
            nome=nome,
            categoria=categoria,
            preco=preco,
            descricao=descricao,
            duracao_estimada=duracao_estimada,
            observacoes=observacoes
        )
        self.servico_repository.add(new_servico)
        return new_servico

    def update_servico(self, servico_id, nome=None, categoria=None, preco=None, descricao=None, duracao_estimada=None, observacoes=None, ativo=None):
        servico = self.servico_repository.get_by_id(servico_id)
        if not servico:
            raise ValueError("Serviço não encontrado")

        if nome is not None:
            nome_existente = self.servico_repository.get_by_nome(nome)
            if nome_existente and nome_existente.id != servico_id:
                raise ValueError("Já existe um serviço com este nome")

        if preco is not None and preco < 0:
            raise ValueError("Preço deve ser um valor positivo")

        if duracao_estimada is not None and duracao_estimada < 0:
            raise ValueError("Duração estimada deve ser um valor positivo")

        servico.nome = nome if nome is not None else servico.nome
        servico.categoria = categoria if categoria is not None else servico.categoria
        servico.preco = preco if preco is not None else servico.preco
        servico.descricao = descricao if descricao is not None else servico.descricao
        servico.duracao_estimada = duracao_estimada if duracao_estimada is not None else servico.duracao_estimada
        servico.observacoes = observacoes if observacoes is not None else servico.observacoes
        servico.ativo = ativo if ativo is not None else servico.ativo
        
        self.servico_repository.update(servico)
        return servico

    def deactivate_servico(self, servico_id):
        servico = self.servico_repository.get_by_id(servico_id)
        if servico:
            servico.ativo = False
            self.servico_repository.update(servico)
            return True
        return False

    def activate_servico(self, servico_id):
        servico = self.servico_repository.get_by_id(servico_id)
        if servico:
            servico.ativo = True
            self.servico_repository.update(servico)
            return servico
        return None

    def get_categorias_disponiveis(self):
        """Retorna as categorias padrão de serviços"""
        return [
            'Banho',
            'Tosa',
            'Consulta Veterinária',
            'Vacinação',
            'Exame',
            'Cirurgia',
            'Hotel',
            'Adestramento',
            'Outros'
        ]

    def get_servicos_estatisticas(self):
        """Retorna estatísticas dos serviços"""
        total_servicos = len(self.get_all_servicos())
        servicos_ativos = len(self.get_active_servicos())
        servicos_inativos = total_servicos - servicos_ativos
        
        # Agrupar por categoria
        servicos = self.get_all_servicos()
        categorias = {}
        for servico in servicos:
            if servico.categoria not in categorias:
                categorias[servico.categoria] = 0
            categorias[servico.categoria] += 1

        return {
            'total': total_servicos,
            'ativos': servicos_ativos,
            'inativos': servicos_inativos,
            'por_categoria': categorias
        }