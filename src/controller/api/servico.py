from flask import Blueprint, jsonify, request
from src.model.models import db, Servico

servico_bp = Blueprint('servico', __name__)

@servico_bp.route('/servicos', methods=['GET'])
def get_servicos():
    """Listar todos os serviços"""
    try:
        servicos = Servico.query.filter_by(ativo=True).all()
        return jsonify([servico.to_dict() for servico in servicos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@servico_bp.route('/servicos', methods=['POST'])
def create_servico():
    """Criar novo serviço"""
    try:
        data = request.json
        
        # Validações básicas
        required_fields = ['nome', 'categoria', 'preco']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'erro': f'{field} é obrigatório'}), 400
        
        # Validar preço
        if data['preco'] < 0:
            return jsonify({'erro': 'Preço não pode ser negativo'}), 400
        
        # Validar duração estimada se fornecida
        if data.get('duracao_estimada') is not None and data['duracao_estimada'] < 0:
            return jsonify({'erro': 'Duração estimada não pode ser negativa'}), 400
        
        servico = Servico(
            nome=data['nome'],
            descricao=data.get('descricao'),
            categoria=data['categoria'],
            preco=data['preco'],
            duracao_estimada=data.get('duracao_estimada'),
            observacoes=data.get('observacoes')
        )
        
        db.session.add(servico)
        db.session.commit()
        
        return jsonify(servico.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@servico_bp.route('/servicos/<int:servico_id>', methods=['GET'])
def get_servico(servico_id):
    """Buscar serviço por ID"""
    try:
        servico = Servico.query.get_or_404(servico_id)
        return jsonify(servico.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@servico_bp.route('/servicos/<int:servico_id>', methods=['PUT'])
def update_servico(servico_id):
    """Atualizar serviço"""
    try:
        servico = Servico.query.get_or_404(servico_id)
        data = request.json
        
        # Validar preço se fornecido
        if data.get('preco') is not None and data['preco'] < 0:
            return jsonify({'erro': 'Preço não pode ser negativo'}), 400
        
        # Validar duração estimada se fornecida
        if data.get('duracao_estimada') is not None and data['duracao_estimada'] < 0:
            return jsonify({'erro': 'Duração estimada não pode ser negativa'}), 400
        
        # Atualizar campos
        servico.nome = data.get('nome', servico.nome)
        servico.descricao = data.get('descricao', servico.descricao)
        servico.categoria = data.get('categoria', servico.categoria)
        servico.preco = data.get('preco', servico.preco)
        servico.duracao_estimada = data.get('duracao_estimada', servico.duracao_estimada)
        servico.observacoes = data.get('observacoes', servico.observacoes)
        
        db.session.commit()
        
        return jsonify(servico.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@servico_bp.route('/servicos/<int:servico_id>', methods=['DELETE'])
def delete_servico(servico_id):
    """Desativar serviço (soft delete)"""
    try:
        servico = Servico.query.get_or_404(servico_id)
        servico.ativo = False
        db.session.commit()
        
        return jsonify({'mensagem': 'Serviço desativado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@servico_bp.route('/servicos/categoria/<categoria>', methods=['GET'])
def get_servicos_by_categoria(categoria):
    """Listar serviços por categoria"""
    try:
        servicos = Servico.query.filter_by(categoria=categoria, ativo=True).all()
        return jsonify([servico.to_dict() for servico in servicos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

