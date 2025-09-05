from flask import Blueprint, jsonify, request
from src.models import db, Pet, Cliente
from datetime import datetime

pet_bp = Blueprint('pet', __name__)

@pet_bp.route('/pets', methods=['GET'])
def get_pets():
    """Listar todos os pets"""
    try:
        pets = Pet.query.filter_by(ativo=True).all()
        return jsonify([pet.to_dict() for pet in pets]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@pet_bp.route('/pets', methods=['POST'])
def create_pet():
    """Criar novo pet"""
    try:
        data = request.json
        
        # Validações básicas
        if not data.get('nome') or not data.get('especie') or not data.get('sexo') or not data.get('cliente_id'):
            return jsonify({'erro': 'Nome, espécie, sexo e cliente_id são obrigatórios'}), 400
        
        # Verificar se cliente existe
        cliente = Cliente.query.get(data['cliente_id'])
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
        
        # Converter data de nascimento se fornecida
        data_nascimento = None
        if data.get('data_nascimento'):
            try:
                data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        pet = Pet(
            nome=data['nome'],
            especie=data['especie'],
            raca=data.get('raca'),
            cor=data.get('cor'),
            sexo=data['sexo'],
            data_nascimento=data_nascimento,
            peso=data.get('peso'),
            observacoes=data.get('observacoes'),
            cliente_id=data['cliente_id']
        )
        
        db.session.add(pet)
        db.session.commit()
        
        return jsonify(pet.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@pet_bp.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    """Buscar pet por ID"""
    try:
        pet = Pet.query.get_or_404(pet_id)
        return jsonify(pet.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@pet_bp.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    """Atualizar pet"""
    try:
        pet = Pet.query.get_or_404(pet_id)
        data = request.json
        
        # Verificar se cliente existe (se fornecido)
        if data.get('cliente_id') and data['cliente_id'] != pet.cliente_id:
            cliente = Cliente.query.get(data['cliente_id'])
            if not cliente:
                return jsonify({'erro': 'Cliente não encontrado'}), 404
        
        # Converter data de nascimento se fornecida
        if data.get('data_nascimento'):
            try:
                data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
                pet.data_nascimento = data_nascimento
            except ValueError:
                return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        # Atualizar campos
        pet.nome = data.get('nome', pet.nome)
        pet.especie = data.get('especie', pet.especie)
        pet.raca = data.get('raca', pet.raca)
        pet.cor = data.get('cor', pet.cor)
        pet.sexo = data.get('sexo', pet.sexo)
        pet.peso = data.get('peso', pet.peso)
        pet.observacoes = data.get('observacoes', pet.observacoes)
        pet.cliente_id = data.get('cliente_id', pet.cliente_id)
        
        db.session.commit()
        
        return jsonify(pet.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@pet_bp.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    """Desativar pet (soft delete)"""
    try:
        pet = Pet.query.get_or_404(pet_id)
        pet.ativo = False
        db.session.commit()
        
        return jsonify({'mensagem': 'Pet desativado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@pet_bp.route('/pets/cliente/<int:cliente_id>', methods=['GET'])
def get_pets_by_cliente(cliente_id):
    """Listar pets de um cliente específico"""
    try:
        pets = Pet.query.filter_by(cliente_id=cliente_id, ativo=True).all()
        return jsonify([pet.to_dict() for pet in pets]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

