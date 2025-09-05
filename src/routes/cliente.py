from flask import Blueprint, jsonify, request
from src.models import db, Cliente
from datetime import datetime

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/clientes', methods=['GET'])
def get_clientes():
    """Listar todos os clientes"""
    try:
        clientes = Cliente.query.filter_by(ativo=True).all()
        return jsonify([cliente.to_dict() for cliente in clientes]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes', methods=['POST'])
def create_cliente():
    """Criar novo cliente"""
    try:
        data = request.json
        
        # Validações básicas
        if not data.get('nome') or not data.get('cpf') or not data.get('telefone'):
            return jsonify({'erro': 'Nome, CPF e telefone são obrigatórios'}), 400
        
        # Verificar se CPF já existe
        if Cliente.query.filter_by(cpf=data['cpf']).first():
            return jsonify({'erro': 'CPF já cadastrado'}), 400
        
        # Verificar se email já existe (se fornecido)
        if data.get('email') and Cliente.query.filter_by(email=data['email']).first():
            return jsonify({'erro': 'Email já cadastrado'}), 400
        
        cliente = Cliente(
            nome=data['nome'],
            cpf=data['cpf'],
            telefone=data['telefone'],
            email=data.get('email'),
            endereco=data.get('endereco')
        )
        
        db.session.add(cliente)
        db.session.commit()
        
        return jsonify(cliente.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    """Buscar cliente por ID"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        return jsonify(cliente.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['PUT'])
def update_cliente(cliente_id):
    """Atualizar cliente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        data = request.json
        
        # Verificar se CPF já existe em outro cliente
        if data.get('cpf') and data['cpf'] != cliente.cpf:
            if Cliente.query.filter_by(cpf=data['cpf']).first():
                return jsonify({'erro': 'CPF já cadastrado'}), 400
        
        # Verificar se email já existe em outro cliente
        if data.get('email') and data['email'] != cliente.email:
            if Cliente.query.filter_by(email=data['email']).first():
                return jsonify({'erro': 'Email já cadastrado'}), 400
        
        # Atualizar campos
        cliente.nome = data.get('nome', cliente.nome)
        cliente.cpf = data.get('cpf', cliente.cpf)
        cliente.telefone = data.get('telefone', cliente.telefone)
        cliente.email = data.get('email', cliente.email)
        cliente.endereco = data.get('endereco', cliente.endereco)
        
        db.session.commit()
        
        return jsonify(cliente.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    """Desativar cliente (soft delete)"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        cliente.ativo = False
        db.session.commit()
        
        return jsonify({'mensagem': 'Cliente desativado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>/pets', methods=['GET'])
def get_cliente_pets(cliente_id):
    """Listar pets de um cliente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        pets = [pet.to_dict() for pet in cliente.pets if pet.ativo]
        return jsonify(pets), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

