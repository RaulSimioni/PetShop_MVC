from flask import Blueprint, jsonify, request
from src.models import db, Venda, ItemVenda, Cliente, Funcionario, Produto, Servico
from datetime import datetime
import uuid

venda_bp = Blueprint('venda', __name__)

@venda_bp.route('/vendas', methods=['GET'])
def get_vendas():
    """Listar todas as vendas"""
    try:
        vendas = Venda.query.all()
        result = []
        for venda in vendas:
            venda_dict = venda.to_dict()
            venda_dict['itens'] = [item.to_dict() for item in venda.itens]
            result.append(venda_dict)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@venda_bp.route('/vendas', methods=['POST'])
def create_venda():
    """Criar nova venda"""
    try:
        data = request.json
        
        # Validações básicas
        required_fields = ['cliente_id', 'funcionario_id', 'forma_pagamento', 'itens']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'erro': f'{field} é obrigatório'}), 400
        
        # Verificar se cliente e funcionário existem
        cliente = Cliente.query.get(data['cliente_id'])
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
        
        funcionario = Funcionario.query.get(data['funcionario_id'])
        if not funcionario:
            return jsonify({'erro': 'Funcionário não encontrado'}), 404
        
        # Validar itens
        if not data['itens'] or len(data['itens']) == 0:
            return jsonify({'erro': 'Pelo menos um item deve ser informado'}), 400
        
        # Gerar número da venda
        numero_venda = f"V{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        
        # Criar venda
        venda = Venda(
            numero_venda=numero_venda,
            cliente_id=data['cliente_id'],
            funcionario_id=data['funcionario_id'],
            forma_pagamento=data['forma_pagamento'],
            desconto=data.get('desconto', 0.0),
            observacoes=data.get('observacoes')
        )
        
        db.session.add(venda)
        db.session.flush()  # Para obter o ID da venda
        
        valor_total = 0.0
        
        # Processar itens
        for item_data in data['itens']:
            if not item_data.get('tipo_item') or item_data['tipo_item'] not in ['produto', 'servico']:
                return jsonify({'erro': 'Tipo de item deve ser "produto" ou "servico"'}), 400
            
            quantidade = item_data.get('quantidade', 1.0)
            if quantidade <= 0:
                return jsonify({'erro': 'Quantidade deve ser maior que zero'}), 400
            
            if item_data['tipo_item'] == 'produto':
                if not item_data.get('produto_id'):
                    return jsonify({'erro': 'produto_id é obrigatório para itens do tipo produto'}), 400
                
                produto = Produto.query.get(item_data['produto_id'])
                if not produto:
                    return jsonify({'erro': f'Produto {item_data["produto_id"]} não encontrado'}), 404
                
                # Verificar estoque
                if produto.estoque_atual < quantidade:
                    return jsonify({'erro': f'Estoque insuficiente para o produto {produto.nome}'}), 400
                
                preco_unitario = item_data.get('preco_unitario', produto.preco_venda)
                subtotal = quantidade * preco_unitario
                
                item_venda = ItemVenda(
                    venda_id=venda.id,
                    produto_id=produto.id,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario,
                    subtotal=subtotal,
                    tipo_item='produto'
                )
                
                # Atualizar estoque
                produto.estoque_atual -= quantidade
                
            else:  # servico
                if not item_data.get('servico_id'):
                    return jsonify({'erro': 'servico_id é obrigatório para itens do tipo servico'}), 400
                
                servico = Servico.query.get(item_data['servico_id'])
                if not servico:
                    return jsonify({'erro': f'Serviço {item_data["servico_id"]} não encontrado'}), 404
                
                preco_unitario = item_data.get('preco_unitario', servico.preco)
                subtotal = quantidade * preco_unitario
                
                item_venda = ItemVenda(
                    venda_id=venda.id,
                    servico_id=servico.id,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario,
                    subtotal=subtotal,
                    tipo_item='servico'
                )
            
            db.session.add(item_venda)
            valor_total += subtotal
        
        # Atualizar valores da venda
        venda.valor_total = valor_total
        venda.valor_final = valor_total - venda.desconto
        
        db.session.commit()
        
        # Retornar venda com itens
        venda_dict = venda.to_dict()
        venda_dict['itens'] = [item.to_dict() for item in venda.itens]
        
        return jsonify(venda_dict), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@venda_bp.route('/vendas/<int:venda_id>', methods=['GET'])
def get_venda(venda_id):
    """Buscar venda por ID"""
    try:
        venda = Venda.query.get_or_404(venda_id)
        venda_dict = venda.to_dict()
        venda_dict['itens'] = [item.to_dict() for item in venda.itens]
        return jsonify(venda_dict), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@venda_bp.route('/vendas/<int:venda_id>/cancelar', methods=['PUT'])
def cancelar_venda(venda_id):
    """Cancelar venda"""
    try:
        venda = Venda.query.get_or_404(venda_id)
        
        if venda.status == 'Cancelada':
            return jsonify({'erro': 'Venda já está cancelada'}), 400
        
        # Reverter estoque dos produtos
        for item in venda.itens:
            if item.tipo_item == 'produto' and item.produto:
                item.produto.estoque_atual += item.quantidade
        
        venda.status = 'Cancelada'
        db.session.commit()
        
        return jsonify({'mensagem': 'Venda cancelada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@venda_bp.route('/vendas/cliente/<int:cliente_id>', methods=['GET'])
def get_vendas_by_cliente(cliente_id):
    """Listar vendas de um cliente"""
    try:
        vendas = Venda.query.filter_by(cliente_id=cliente_id).all()
        result = []
        for venda in vendas:
            venda_dict = venda.to_dict()
            venda_dict['itens'] = [item.to_dict() for item in venda.itens]
            result.append(venda_dict)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

