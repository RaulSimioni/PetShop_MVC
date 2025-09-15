from flask import Blueprint, jsonify, request
from src.model.services.cliente_service import ClienteService

cliente_bp = Blueprint("cliente_api", __name__)
cliente_service = ClienteService()

@cliente_bp.route("/clientes", methods=["GET"])
def get_clientes():
    """Listar todos os clientes"""
    try:
        clientes = cliente_service.get_all_clientes()
        return jsonify([cliente.to_dict() for cliente in clientes]), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@cliente_bp.route("/clientes", methods=["POST"])
def create_cliente():
    """Criar novo cliente"""
    try:
        data = request.json

        cliente = cliente_service.create_cliente(
            nome=data.get("nome"),
            cpf=data.get("cpf"),
            telefone=data.get("telefone"),
            email=data.get("email"),
            endereco=data.get("endereco"),
        )

        return jsonify(cliente.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@cliente_bp.route("/clientes/<int:cliente_id>", methods=["GET"])
def get_cliente(cliente_id):
    """Buscar cliente por ID"""
    try:
        cliente = cliente_service.get_cliente_by_id(cliente_id)
        if not cliente:
            return jsonify({"erro": "Cliente não encontrado"}), 404
        return jsonify(cliente.to_dict()), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@cliente_bp.route("/clientes/<int:cliente_id>", methods=["PUT"])
def update_cliente(cliente_id):
    """Atualizar cliente"""
    try:
        data = request.json

        cliente = cliente_service.update_cliente(
            cliente_id=cliente_id,
            nome=data.get("nome"),
            cpf=data.get("cpf"),
            telefone=data.get("telefone"),
            email=data.get("email"),
            endereco=data.get("endereco"),
            ativo=data.get("ativo"),
        )

        return jsonify(cliente.to_dict()), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@cliente_bp.route("/clientes/<int:cliente_id>", methods=["DELETE"])
def delete_cliente(cliente_id):
    """Desativar cliente (soft delete)"""
    try:
        if cliente_service.deactivate_cliente(cliente_id):
            return jsonify({"mensagem": "Cliente desativado com sucesso"}), 200
        return jsonify({"erro": "Cliente não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@cliente_bp.route("/clientes/<int:cliente_id>/ativar", methods=["PUT"])
def activate_cliente(cliente_id):
    """Ativar cliente"""
    try:
        cliente = cliente_service.activate_cliente(cliente_id)
        if not cliente:
            return jsonify({"erro": "Cliente não encontrado"}), 404
        return jsonify(cliente.to_dict()), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@cliente_bp.route("/clientes/<int:cliente_id>/pets", methods=["GET"])
def get_cliente_pets(cliente_id):
    """Listar pets de um cliente"""
    try:
        pets = cliente_service.get_pets_by_cliente_id(cliente_id)
        if pets is None:
            return jsonify({"erro": "Cliente não encontrado"}), 404
        return jsonify([pet.to_dict() for pet in pets]), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500



