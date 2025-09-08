from flask import Blueprint, jsonify, request
from src.model.models import db, Produto

produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/produtos', methods=['GET'])
def get_produtos():
    """Listar todos os produtos"""
    try:
        produtos = Produto.query.filter_by(ativo=True).all()
        return jsonify([produto.to_dict() for produto in produtos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos', methods=['POST'])
def create_produto():
    """Criar novo produto"""
    try:
        data = request.json
        
        # Validações básicas
        required_fields = ['nome', 'categoria', 'preco_custo', 'preco_venda']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'erro': f'{field} é obrigatório'}), 400
        
        # Verificar se código de barras já existe (se fornecido)
        if data.get('codigo_barras'):
            if Produto.query.filter_by(codigo_barras=data['codigo_barras']).first():
                return jsonify({'erro': 'Código de barras já cadastrado'}), 400
        
        # Validar preços
        if data['preco_custo'] < 0 or data['preco_venda'] < 0:
            return jsonify({'erro': 'Preços não podem ser negativos'}), 400
        
        produto = Produto(
            nome=data['nome'],
            descricao=data.get('descricao'),
            categoria=data['categoria'],
            marca=data.get('marca'),
            codigo_barras=data.get('codigo_barras'),
            preco_custo=data['preco_custo'],
            preco_venda=data['preco_venda'],
            estoque_atual=data.get('estoque_atual', 0),
            estoque_minimo=data.get('estoque_minimo', 0),
            unidade_medida=data.get('unidade_medida', 'UN')
        )
        
        db.session.add(produto)
        db.session.commit()
        
        return jsonify(produto.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos/<int:produto_id>', methods=['GET'])
def get_produto(produto_id):
    """Buscar produto por ID"""
    try:
        produto = Produto.query.get_or_404(produto_id)
        return jsonify(produto.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    """Atualizar produto"""
    try:
        produto = Produto.query.get_or_404(produto_id)
        data = request.json
        
        # Verificar se código de barras já existe em outro produto
        if data.get('codigo_barras') and data['codigo_barras'] != produto.codigo_barras:
            if Produto.query.filter_by(codigo_barras=data['codigo_barras']).first():
                return jsonify({'erro': 'Código de barras já cadastrado'}), 400
        
        # Validar preços se fornecidos
        if data.get('preco_custo') is not None and data['preco_custo'] < 0:
            return jsonify({'erro': 'Preço de custo não pode ser negativo'}), 400
        
        if data.get('preco_venda') is not None and data['preco_venda'] < 0:
            return jsonify({'erro': 'Preço de venda não pode ser negativo'}), 400
        
        # Atualizar campos
        produto.nome = data.get('nome', produto.nome)
        produto.descricao = data.get('descricao', produto.descricao)
        produto.categoria = data.get('categoria', produto.categoria)
        produto.marca = data.get('marca', produto.marca)
        produto.codigo_barras = data.get('codigo_barras', produto.codigo_barras)
        produto.preco_custo = data.get('preco_custo', produto.preco_custo)
        produto.preco_venda = data.get('preco_venda', produto.preco_venda)
        produto.estoque_atual = data.get('estoque_atual', produto.estoque_atual)
        produto.estoque_minimo = data.get('estoque_minimo', produto.estoque_minimo)
        produto.unidade_medida = data.get('unidade_medida', produto.unidade_medida)
        
        db.session.commit()
        
        return jsonify(produto.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    """Desativar produto (soft delete)"""
    try:
        produto = Produto.query.get_or_404(produto_id)
        produto.ativo = False
        db.session.commit()
        
        return jsonify({'mensagem': 'Produto desativado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos/estoque-baixo', methods=['GET'])
def get_produtos_estoque_baixo():
    """Listar produtos com estoque baixo"""
    try:
        produtos = Produto.query.filter(
            Produto.ativo == True,
            Produto.estoque_atual <= Produto.estoque_minimo
        ).all()
        return jsonify([produto.to_dict() for produto in produtos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos/categoria/<categoria>', methods=['GET'])
def get_produtos_by_categoria(categoria):
    """Listar produtos por categoria"""
    try:
        produtos = Produto.query.filter_by(categoria=categoria, ativo=True).all()
        return jsonify([produto.to_dict() for produto in produtos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

