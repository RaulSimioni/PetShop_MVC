import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, send_from_directory, render_template, session, redirect, url_for, flash, request
from functools import wraps
from flask_cors import CORS
from src.model.models import db
from src.model.services.cliente_service import ClienteService

# Importar rotas de API (backend - JSON)
from src.controller.api.user import user_bp
from src.controller.api.cliente import cliente_bp
from src.controller.api.pet import pet_bp
from src.controller.api.funcionario import funcionario_bp
from src.controller.api.servico import servico_bp
from src.controller.api.agendamento import agendamento_bp

# Importar views (frontend - HTML templates)
from src.controller.views.cliente import cliente_views_bp
from src.controller.views.pet import pet_views_bp
from src.controller.views.funcionario import funcionario_views_bp
from src.controller.views.servico import servico_views_bp
from src.controller.views.agendamento import agendamento_views_bp
from src.controller.views.auth import auth_views_bp

app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(__file__), 'view', 'static'),
            template_folder=os.path.join(os.path.dirname(__file__), 'view', 'templates'))

# Configurações
app.config['SECRET_KEY'] = 'petshop_erp_secret_key_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'model', 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurar CORS para permitir requisições de qualquer origem
CORS(app, origins="*")

# Registrar blueprints de API (backend - JSON endpoints)
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(cliente_bp, url_prefix='/api')
app.register_blueprint(pet_bp, url_prefix='/api')
app.register_blueprint(funcionario_bp, url_prefix='/api')
app.register_blueprint(servico_bp, url_prefix='/api')
app.register_blueprint(agendamento_bp, url_prefix='/api')

# Registrar blueprints de Views (frontend - HTML templates)
app.register_blueprint(cliente_views_bp)  # Sem prefixo /api
app.register_blueprint(pet_views_bp)  # Sem prefixo /api
app.register_blueprint(funcionario_views_bp)  # Sem prefixo /api
app.register_blueprint(servico_views_bp)  # Sem prefixo /api
app.register_blueprint(agendamento_views_bp)  # Sem prefixo /api
app.register_blueprint(auth_views_bp)  # Sem prefixo /api

# Inicializar banco de dados
db.init_app(app)

# Criar tabelas
with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth_views.login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def before_request():
    if request.endpoint and 'static' not in request.endpoint and request.endpoint != 'auth_views.login' and request.endpoint != 'auth_views.register' and request.endpoint != 'api_info':
        if 'logged_in' not in session or not session['logged_in']:
            if request.blueprint == 'auth_views':
                pass
            elif request.blueprint == 'api':
                pass
            else:
                return redirect(url_for('auth_views.login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal do sistema"""
    from src.model.models import Cliente, Pet, Funcionario, Servico, Agendamento
    from datetime import datetime, date
    
    try:
        # Estatísticas básicas usando query direta
        total_clientes = Cliente.query.count()
        clientes_ativos = Cliente.query.filter_by(ativo=True).count()
        
        total_pets = Pet.query.count()
        pets_ativos = Pet.query.filter_by(ativo=True).count()
        
        total_funcionarios = Funcionario.query.count()
        funcionarios_ativos = Funcionario.query.filter_by(ativo=True).count()
        
        total_servicos = Servico.query.count()
        servicos_ativos = Servico.query.filter_by(ativo=True).count()

        # Agendamentos
        total_agendamentos = Agendamento.query.count()
        
        # Agendamentos de hoje
        hoje = date.today()
        agendamentos_hoje = Agendamento.query.filter(
            db.func.date(Agendamento.data_agendamento) == hoje
        ).all()
        
        # Agendamentos pendentes (agendado, confirmado, em_andamento)
        status_pendentes = ['agendado', 'confirmado', 'em_andamento']
        agendamentos_pendentes = Agendamento.query.filter(
            Agendamento.status.in_(status_pendentes)
        ).count()

        stats = {
            'total_clientes': total_clientes,
            'clientes_ativos': clientes_ativos,
            'total_pets': total_pets,
            'pets_ativos': pets_ativos,
            'total_funcionarios': total_funcionarios,
            'funcionarios_ativos': funcionarios_ativos,
            'total_servicos': total_servicos,
            'servicos_ativos': servicos_ativos,
            'total_agendamentos': total_agendamentos,
            'agendamentos_hoje': len(agendamentos_hoje),
            'agendamentos_pendentes': agendamentos_pendentes
        }
        
        # Dados recentes para exibição
        clientes_recentes = Cliente.query.filter_by(ativo=True).order_by(Cliente.data_cadastro.desc()).limit(5).all()
        agendamentos_hoje_lista = agendamentos_hoje[:5]  # Mostrar apenas os primeiros 5
        
        return render_template('dashboard.html', 
                             stats=stats,
                             clientes_recentes=clientes_recentes,
                             agendamentos_hoje=agendamentos_hoje_lista)
                             
    except Exception as e:
        print(f"Erro no dashboard: {e}")
        # Em caso de erro, retornar dashboard com dados vazios
        stats = {
            'total_clientes': 0,
            'clientes_ativos': 0,
            'total_pets': 0,
            'pets_ativos': 0,
            'total_funcionarios': 0,
            'funcionarios_ativos': 0,
            'total_servicos': 0,
            'servicos_ativos': 0,
            'total_agendamentos': 0,
            'agendamentos_hoje': 0,
            'agendamentos_pendentes': 0
        }
        return render_template('dashboard.html', 
                             stats=stats,
                             clientes_recentes=[],
                             agendamentos_hoje=[])

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Servir arquivos estáticos ou redirecionar para dashboard"""
    static_folder_path = app.static_folder
    
    # Se path está vazio, redirecionar para dashboard
    if not path or path == 'index.html':
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('auth_views.login'))
        return dashboard()
    
    if static_folder_path is None:
        return "Static folder not configured", 404

    if os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        # Se arquivo não existe, verificar se existe index.html
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            # Redirecionar para dashboard como fallback
            return dashboard()

@app.route('/api')
def api_info():
    """Informações sobre as rotas da API"""
    routes_info = {
        "message": "Sistema ERP Pet Shop - API REST",
        "version": "1.0.0",
        "endpoints": {
            "clientes": {
                "GET /api/clientes": "Listar todos os clientes",
                "POST /api/clientes": "Criar novo cliente",
                "GET /api/clientes/{id}": "Buscar cliente por ID",
                "PUT /api/clientes/{id}": "Atualizar cliente",
                "DELETE /api/clientes/{id}": "Desativar cliente",
                "GET /api/clientes/{id}/pets": "Listar pets do cliente"
            },
            "pets": {
                "GET /api/pets": "Listar todos os pets",
                "POST /api/pets": "Criar novo pet",
                "GET /api/pets/{id}": "Buscar pet por ID",
                "PUT /api/pets/{id}": "Atualizar pet",
                "DELETE /api/pets/{id}": "Desativar pet",
                "GET /api/pets/cliente/{cliente_id}": "Listar pets por cliente"
            },
            "funcionarios": {
                "GET /api/funcionarios": "Listar todos os funcionários",
                "POST /api/funcionarios": "Criar novo funcionário",
                "GET /api/funcionarios/{id}": "Buscar funcionário por ID",
                "PUT /api/funcionarios/{id}": "Atualizar funcionário",
                "DELETE /api/funcionarios/{id}": "Desativar funcionário"
            },
            "servicos": {
                "GET /api/servicos": "Listar todos os serviços",
                "POST /api/servicos": "Criar novo serviço",
                "GET /api/servicos/{id}": "Buscar serviço por ID",
                "PUT /api/servicos/{id}": "Atualizar serviço",
                "DELETE /api/servicos/{id}": "Desativar serviço",
                "GET /api/servicos/categoria/{categoria}": "Serviços por categoria"
            },
            "agendamentos": {
                "GET /api/agendamentos": "Listar agendamentos (com filtros opcionais)",
                "POST /api/agendamentos": "Criar novo agendamento",
                "GET /api/agendamentos/{id}": "Buscar agendamento por ID",
                "PUT /api/agendamentos/{id}": "Atualizar agendamento",
                "PUT /api/agendamentos/{id}/status": "Atualizar status do agendamento",
                "DELETE /api/agendamentos/{id}": "Cancelar agendamento",
                "GET /api/agendamentos/cliente/{cliente_id}": "Agendamentos por cliente",
                "GET /api/agendamentos/funcionario/{funcionario_id}": "Agendamentos por funcionário"
            }
        }
    }
    return routes_info

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
