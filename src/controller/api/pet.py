from flask import Blueprint, jsonify, request
from src.model.services.pet_service import PetService
from datetime import datetime

pet_bp = Blueprint("pet_api", __name__)
pet_service = PetService()

@pet_bp.route("/pets", methods=["GET"])
def get_pets():
    """Listar todos os pets"""
    try:
        cliente_id = request.args.get("cliente_id", type=int)
        if cliente_id:
            pets = pet_service.get_pets_by_cliente_id(cliente_id)
        else:
            pets = pet_service.get_all_pets()
        return jsonify([pet.to_dict() for pet in pets]), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@pet_bp.route("/pets", methods=["POST"])
def create_pet():
    """Criar novo pet"""
    try:
        data = request.json

        # Converter data_nascimento se fornecida
        data_nascimento = None
        if data.get("data_nascimento"):
            try:
                data_nascimento = datetime.strptime(data.get("data_nascimento"), "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"erro": "Formato de data inválido. Use YYYY-MM-DD"}), 400

        pet = pet_service.create_pet(
            nome=data.get("nome"),
            especie=data.get("especie"),
            cliente_id=data.get("cliente_id"),
            raca=data.get("raca"),
            cor=data.get("cor"),
            sexo=data.get("sexo"),
            data_nascimento=data_nascimento,
            peso=data.get("peso"),
            observacoes=data.get("observacoes"),
        )

        return jsonify(pet.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@pet_bp.route("/pets/<int:pet_id>", methods=["GET"])
def get_pet(pet_id):
    """Buscar pet por ID"""
    try:
        pet = pet_service.get_pet_by_id(pet_id)
        if not pet:
            return jsonify({"erro": "Pet não encontrado"}), 404
        return jsonify(pet.to_dict()), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@pet_bp.route("/pets/<int:pet_id>", methods=["PUT"])
def update_pet(pet_id):
    """Atualizar pet"""
    try:
        data = request.json

        # Converter data_nascimento se fornecida
        data_nascimento = None
        if data.get("data_nascimento"):
            try:
                data_nascimento = datetime.strptime(data.get("data_nascimento"), "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"erro": "Formato de data inválido. Use YYYY-MM-DD"}), 400

        pet = pet_service.update_pet(
            pet_id=pet_id,
            nome=data.get("nome"),
            especie=data.get("especie"),
            raca=data.get("raca"),
            cor=data.get("cor"),
            sexo=data.get("sexo"),
            data_nascimento=data_nascimento,
            peso=data.get("peso"),
            observacoes=data.get("observacoes"),
            ativo=data.get("ativo"),
            cliente_id=data.get("cliente_id"),
        )

        return jsonify(pet.to_dict()), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@pet_bp.route("/pets/<int:pet_id>", methods=["DELETE"])
def delete_pet(pet_id):
    """Desativar pet (soft delete)"""
    try:
        if pet_service.deactivate_pet(pet_id):
            return jsonify({"mensagem": "Pet desativado com sucesso"}), 200
        return jsonify({"erro": "Pet não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@pet_bp.route("/pets/<int:pet_id>/ativar", methods=["PUT"])
def activate_pet(pet_id):
    """Ativar pet"""
    try:
        pet = pet_service.activate_pet(pet_id)
        if not pet:
            return jsonify({"erro": "Pet não encontrado"}), 404
        return jsonify(pet.to_dict()), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@pet_bp.route("/pets/especies", methods=["GET"])
def get_especies():
    """Listar espécies disponíveis"""
    try:
        especies = pet_service.get_especies_disponiveis()
        return jsonify({"especies": especies}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@pet_bp.route("/pets/sexos", methods=["GET"])
def get_sexos():
    """Listar sexos disponíveis"""
    try:
        sexos = pet_service.get_sexos_disponiveis()
        return jsonify({"sexos": sexos}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

