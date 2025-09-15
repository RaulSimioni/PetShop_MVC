from flask_sqlalchemy import SQLAlchemy

# Instância única do SQLAlchemy
db = SQLAlchemy()

# Importar todos os modelos
from .cliente import Cliente
from .pet import Pet
from .funcionario import Funcionario
from .servico import Servico
from .agendamento import Agendamento
from .user import User

# Exportar todos os modelos
__all__ = [
    'db',
    'Cliente',
    'Pet', 
    'Funcionario',
    'Servico',
    'Agendamento',
    'User'
]

