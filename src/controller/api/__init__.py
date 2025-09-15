# API Routes - Backend endpoints que retornam JSON
# Todos os arquivos nesta pasta são rotas de API REST

from .cliente import cliente_bp
from .user import user_bp
from .pet import pet_bp
from .funcionario import funcionario_bp
from .servico import servico_bp
from .agendamento import agendamento_bp

__all__ = [
    'cliente_bp',
    'user_bp', 
    'pet_bp',
    'funcionario_bp',
    'servico_bp',
    'agendamento_bp'
]
