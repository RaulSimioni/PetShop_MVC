import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models import db
from src.routes.user import user_bp
from src.routes.cliente import cliente_bp
from src.routes.pet import pet_bp
from src.routes.funcionario import funcionario_bp
from src.routes.produto import produto_bp
from src.routes.servico import servico_bp
from src.routes.venda import venda_bp
from src.routes.agendamento import agendamento_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações
app.config['SECRET_KEY'] = 'petshop_erp_secret_key_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurar CORS para permitir requisições de qualquer origem
CORS(app, origins="*")

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(cliente_bp, url_prefix='/api')
app.register_blueprint(pet_bp, url_prefix='/api')
app.register_blueprint(funcionario_bp, url_prefix='/api')
app.register_blueprint(produto_bp, url_prefix='/api')
app.register_blueprint(servico_bp, url_prefix='/api')
app.register_blueprint(venda_bp, url_prefix='/api')
app.register_blueprint(agendamento_bp, url_prefix='/api')

# Inicializar banco de dados
db.init_app(app)

# Criar tabelas
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Servir arquivos estáticos (frontend)"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "Sistema ERP Pet Shop - Backend funcionando! Acesse /api para ver as rotas disponíveis.", 200

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
            "produtos": {
                "GET /api/produtos": "Listar todos os produtos",
                "POST /api/produtos": "Criar novo produto",
                "GET /api/produtos/{id}": "Buscar produto por ID",
                "PUT /api/produtos/{id}": "Atualizar produto",
                "DELETE /api/produtos/{id}": "Desativar produto",
                "GET /api/produtos/estoque-baixo": "Produtos com estoque baixo",
                "GET /api/produtos/categoria/{categoria}": "Produtos por categoria"
            },
            "servicos": {
                "GET /api/servicos": "Listar todos os serviços",
                "POST /api/servicos": "Criar novo serviço",
                "GET /api/servicos/{id}": "Buscar serviço por ID",
                "PUT /api/servicos/{id}": "Atualizar serviço",
                "DELETE /api/servicos/{id}": "Desativar serviço",
                "GET /api/servicos/categoria/{categoria}": "Serviços por categoria"
            },
            "vendas": {
                "GET /api/vendas": "Listar todas as vendas",
                "POST /api/vendas": "Criar nova venda",
                "GET /api/vendas/{id}": "Buscar venda por ID",
                "PUT /api/vendas/{id}/cancelar": "Cancelar venda",
                "GET /api/vendas/cliente/{cliente_id}": "Vendas por cliente"
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

