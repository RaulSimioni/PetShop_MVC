from flask import Blueprint, jsonify, request
from src.models import db, Funcionario
from datetime import datetime

funcionario_bp = Blueprint('funcionario', __name__)

@funcionario_bp.route('/funcionarios', methods=['GET'])
def get_funcionarios():
    """Listar todos os funcionários"""
    try:
        funcionarios = Funcionario.query.filter_by(ativo=True).all()
        return jsonify([funcionario.to_dict() for funcionario in funcionarios]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@funcionario_bp.route('/funcionarios', methods=['POST'])
def create_funcionario():
    """Criar novo funcionário"""
    try:
        data = request.json
        
        # Validações básicas
        required_fields = ['nome', 'cpf', 'telefone', 'cargo', 'data_admissao']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'erro': f'{field} é obrigatório'}), 400
        
        # Verificar se CPF já existe
        if Funcionario.query.filter_by(cpf=data['cpf']).first():
            return jsonify({'erro': 'CPF já cadastrado'}), 400
        
        # Verificar se email já existe (se fornecido)
        if data.get('email') and Funcionario.query.filter_by(email=data['email']).first():
            return jsonify({'erro': 'Email já cadastrado'}), 400
        
        # Converter data de admissão
        try:
            data_admissao = datetime.strptime(data['data_admissao'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'erro': 'Formato de data de admissão inválido. Use YYYY-MM-DD'}), 400
        
        # Converter data de demissão se fornecida
        data_demissao = None
        if data.get('data_demissao'):
            try:
                data_demissao = datetime.strptime(data['data_demissao'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'erro': 'Formato de data de demissão inválido. Use YYYY-MM-DD'}), 400
        
        funcionario = Funcionario(
            nome=data['nome'],
            cpf=data['cpf'],
            telefone=data['telefone'],
            email=data.get('email'),
            endereco=data.get('endereco'),
            cargo=data['cargo'],
            salario=data.get('salario'),
            data_admissao=data_admissao,
            data_demissao=data_demissao
        )
        
        db.session.add(funcionario)
        db.session.commit()
        
        return jsonify(funcionario.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@funcionario_bp.route('/funcionarios/<int:funcionario_id>', methods=['GET'])
def get_funcionario(funcionario_id):
    """Buscar funcionário por ID"""
    try:
        funcionario = Funcionario.query.get_or_404(funcionario_id)
        return jsonify(funcionario.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@funcionario_bp.route('/funcionarios/<int:funcionario_id>', methods=['PUT'])
def update_funcionario(funcionario_id):
    """Atualizar funcionário"""
    try:
        funcionario = Funcionario.query.get_or_404(funcionario_id)
        data = request.json
        
        # Verificar se CPF já existe em outro funcionário
        if data.get('cpf') and data['cpf'] != funcionario.cpf:
            if Funcionario.query.filter_by(cpf=data['cpf']).first():
                return jsonify({'erro': 'CPF já cadastrado'}), 400
        
        # Verificar se email já existe em outro funcionário
        if data.get('email') and data['email'] != funcionario.email:
            if Funcionario.query.filter_by(email=data['email']).first():
                return jsonify({'erro': 'Email já cadastrado'}), 400
        
        # Converter datas se fornecidas
        if data.get('data_admissao'):
            try:
                funcionario.data_admissao = datetime.strptime(data['data_admissao'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'erro': 'Formato de data de admissão inválido. Use YYYY-MM-DD'}), 400
        
        if data.get('data_demissao'):
            try:
                funcionario.data_demissao = datetime.strptime(data['data_demissao'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'erro': 'Formato de data de demissão inválido. Use YYYY-MM-DD'}), 400
        
        # Atualizar campos
        funcionario.nome = data.get('nome', funcionario.nome)
        funcionario.cpf = data.get('cpf', funcionario.cpf)
        funcionario.telefone = data.get('telefone', funcionario.telefone)
        funcionario.email = data.get('email', funcionario.email)
        funcionario.endereco = data.get('endereco', funcionario.endereco)
        funcionario.cargo = data.get('cargo', funcionario.cargo)
        funcionario.salario = data.get('salario', funcionario.salario)
        
        db.session.commit()
        
        return jsonify(funcionario.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@funcionario_bp.route('/funcionarios/<int:funcionario_id>', methods=['DELETE'])
def delete_funcionario(funcionario_id):
    """Desativar funcionário (soft delete)"""
    try:
        funcionario = Funcionario.query.get_or_404(funcionario_id)
        funcionario.ativo = False
        db.session.commit()
        
        return jsonify({'mensagem': 'Funcionário desativado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

