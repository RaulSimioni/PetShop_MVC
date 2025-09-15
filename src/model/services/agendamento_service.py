from src.model.repositories.agendamento_repository import AgendamentoRepository
from src.model.models import Agendamento
from src.model.services.cliente_service import ClienteService
from src.model.services.funcionario_service import FuncionarioService
from src.model.services.servico_service import ServicoService
from datetime import datetime, timedelta

class AgendamentoService:
    def __init__(self):
        self.agendamento_repository = AgendamentoRepository()
        self.cliente_service = ClienteService()
        self.funcionario_service = FuncionarioService()
        self.servico_service = ServicoService()

    def get_all_agendamentos(self):
        return self.agendamento_repository.get_all()

    def get_agendamento_by_id(self, agendamento_id):
        return self.agendamento_repository.get_by_id(agendamento_id)

    def get_agendamentos_by_cliente(self, cliente_id):
        return self.agendamento_repository.get_by_cliente_id(cliente_id)

    def get_agendamentos_by_funcionario(self, funcionario_id):
        return self.agendamento_repository.get_by_funcionario_id(funcionario_id)

    def get_agendamentos_by_servico(self, servico_id):
        return self.agendamento_repository.get_by_servico_id(servico_id)

    def get_agendamentos_by_status(self, status):
        return self.agendamento_repository.get_by_status(status)

    def get_agendamentos_by_date_range(self, data_inicio, data_fim):
        return self.agendamento_repository.get_by_date_range(data_inicio, data_fim)

    def create_agendamento(self, cliente_id, servico_id, data_agendamento, 
                          funcionario_id=None, pet_id=None, observacoes=None, valor_estimado=None):
        # Validações básicas
        if not cliente_id or not servico_id or not data_agendamento:
            raise ValueError("Cliente, serviço e data do agendamento são obrigatórios")

        # Verificar se cliente existe e está ativo
        cliente = self.cliente_service.get_cliente_by_id(cliente_id)
        if not cliente or not cliente.ativo:
            raise ValueError("Cliente não encontrado ou inativo")

        # Verificar se serviço existe e está ativo
        servico = self.servico_service.get_servico_by_id(servico_id)
        if not servico or not servico.ativo:
            raise ValueError("Serviço não encontrado ou inativo")

        # Verificar se funcionário existe e está ativo (se fornecido)
        if funcionario_id:
            funcionario = self.funcionario_service.get_funcionario_by_id(funcionario_id)
            if not funcionario or not funcionario.ativo:
                raise ValueError("Funcionário não encontrado ou inativo")

        # Verificar se a data não é no passado
        if isinstance(data_agendamento, str):
            data_agendamento = datetime.fromisoformat(data_agendamento)
        
        if data_agendamento < datetime.now():
            raise ValueError("Não é possível agendar para datas passadas")

        # Calcular tempo estimado baseado no serviço
        tempo_estimado = servico.duracao_estimada if servico.duracao_estimada else None

        # Usar valor do serviço como estimativa se não fornecido
        if valor_estimado is None:
            valor_estimado = servico.preco

        new_agendamento = Agendamento(
            cliente_id=cliente_id,
            servico_id=servico_id,
            data_agendamento=data_agendamento,
            funcionario_id=funcionario_id,
            pet_id=pet_id,
            observacoes=observacoes,
            valor_estimado=valor_estimado,
            tempo_estimado=tempo_estimado,
            status='Agendado'
        )
        
        self.agendamento_repository.add(new_agendamento)
        return new_agendamento

    def update_agendamento(self, agendamento_id, **kwargs):
        agendamento = self.agendamento_repository.get_by_id(agendamento_id)
        if not agendamento:
            raise ValueError("Agendamento não encontrado")

        # Validar campos se fornecidos
        if 'cliente_id' in kwargs and kwargs['cliente_id']:
            cliente = self.cliente_service.get_cliente_by_id(kwargs['cliente_id'])
            if not cliente or not cliente.ativo:
                raise ValueError("Cliente não encontrado ou inativo")

        if 'servico_id' in kwargs and kwargs['servico_id']:
            servico = self.servico_service.get_servico_by_id(kwargs['servico_id'])
            if not servico or not servico.ativo:
                raise ValueError("Serviço não encontrado ou inativo")

        if 'funcionario_id' in kwargs and kwargs['funcionario_id']:
            funcionario = self.funcionario_service.get_funcionario_by_id(kwargs['funcionario_id'])
            if not funcionario or not funcionario.ativo:
                raise ValueError("Funcionário não encontrado ou inativo")

        if 'data_agendamento' in kwargs and kwargs['data_agendamento']:
            data_agendamento = kwargs['data_agendamento']
            if isinstance(data_agendamento, str):
                data_agendamento = datetime.fromisoformat(data_agendamento)
            if data_agendamento < datetime.now():
                raise ValueError("Não é possível agendar para datas passadas")

        # Atualizar campos
        for key, value in kwargs.items():
            if hasattr(agendamento, key) and value is not None:
                setattr(agendamento, key, value)

        self.agendamento_repository.update(agendamento)
        return agendamento

    def update_status(self, agendamento_id, status):
        valid_statuses = ['Agendado', 'Confirmado', 'Em Andamento', 'Concluído', 'Cancelado']
        if status not in valid_statuses:
            raise ValueError(f"Status inválido. Use um dos seguintes: {', '.join(valid_statuses)}")

        agendamento = self.agendamento_repository.get_by_id(agendamento_id)
        if not agendamento:
            raise ValueError("Agendamento não encontrado")

        agendamento.status = status
        self.agendamento_repository.update(agendamento)
        return agendamento

    def cancel_agendamento(self, agendamento_id):
        return self.update_status(agendamento_id, 'Cancelado')

    def confirm_agendamento(self, agendamento_id):
        return self.update_status(agendamento_id, 'Confirmado')

    def start_agendamento(self, agendamento_id):
        return self.update_status(agendamento_id, 'Em Andamento')

    def complete_agendamento(self, agendamento_id):
        return self.update_status(agendamento_id, 'Concluído')

    def get_agendamentos_hoje(self):
        hoje = datetime.now().date()
        inicio_dia = datetime.combine(hoje, datetime.min.time())
        fim_dia = datetime.combine(hoje, datetime.max.time())
        return self.get_agendamentos_by_date_range(inicio_dia, fim_dia)

    def get_agendamentos_semana(self):
        hoje = datetime.now().date()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        inicio_dia = datetime.combine(inicio_semana, datetime.min.time())
        fim_dia = datetime.combine(fim_semana, datetime.max.time())
        return self.get_agendamentos_by_date_range(inicio_dia, fim_dia)

    def get_status_disponiveis(self):
        return ['Agendado', 'Confirmado', 'Em Andamento', 'Concluído', 'Cancelado']

    def get_agendamentos_estatisticas(self):
        """Retorna estatísticas dos agendamentos"""
        agendamentos = self.get_all_agendamentos()
        
        total = len(agendamentos)
        
        # Contar por status
        status_count = {}
        for agendamento in agendamentos:
            status = agendamento.status
            status_count[status] = status_count.get(status, 0) + 1

        # Agendamentos de hoje
        agendamentos_hoje = self.get_agendamentos_hoje()
        
        # Agendamentos da semana
        agendamentos_semana = self.get_agendamentos_semana()

        return {
            'total': total,
            'hoje': len(agendamentos_hoje),
            'semana': len(agendamentos_semana),
            'por_status': status_count,
            'agendados': status_count.get('Agendado', 0),
            'confirmados': status_count.get('Confirmado', 0),
            'em_andamento': status_count.get('Em Andamento', 0),
            'concluidos': status_count.get('Concluído', 0),
            'cancelados': status_count.get('Cancelado', 0)
        }