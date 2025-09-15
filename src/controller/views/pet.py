from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.model.services.pet_service import PetService
from src.model.services.cliente_service import ClienteService
from datetime import datetime
import math

pet_views_bp = Blueprint("pet_views", __name__)
pet_service = PetService()
cliente_service = ClienteService()

@pet_views_bp.route("/pets")
def listar_pets():
    """Página de listagem de pets"""
    page = request.args.get("page", 1, type=int)
    per_page = 10
    search = request.args.get("search", "", type=str)
    status = request.args.get("status", "", type=str)
    especie = request.args.get("especie", "", type=str)
    cliente_id = request.args.get("cliente_id", type=int)

    try:
        # Buscar todos os pets
        if cliente_id:
            pets = pet_service.get_pets_by_cliente_id(cliente_id)
        else:
            pets = pet_service.get_all_pets()

        # Filtros
        if search:
            pets = [p for p in pets if search.lower() in p.nome.lower() or 
                   search.lower() in p.dono.nome.lower() or 
                   (p.raca and search.lower() in p.raca.lower())]
        
        if status == 'true':
            pets = [p for p in pets if p.ativo]
        elif status == 'false':
            pets = [p for p in pets if not p.ativo]

        if especie:
            pets = [p for p in pets if p.especie == especie]

        total_pets = len(pets)
        total_pages = math.ceil(total_pets / per_page)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        pets_paginados = pets[start_index:end_index]

        # Criar objeto de paginação simulado
        class Pagination:
            def __init__(self, page, per_page, total_count, items):
                self.page = page
                self.per_page = per_page
                self.total = total_count
                self.items = items
                self.pages = math.ceil(total_count / per_page)
                self.has_next = self.page < self.pages
                self.has_prev = self.page > 1

            def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
                last_page = self.pages
                for num in range(1, last_page + 1):
                    if num <= left_edge or \
                       (num > self.page - left_current - 1 and num < self.page + right_current) or \
                       num > last_page - right_edge:
                        yield num

        pagination = Pagination(page, per_page, total_pets, pets_paginados)

        # Dados para filtros
        especies = pet_service.get_especies_disponiveis()
        
        return render_template("pets/listar.html", 
                             pets=pets_paginados, 
                             pagination=pagination, 
                             search=search, 
                             status=status,
                             especie=especie,
                             especies=especies,
                             cliente_id=cliente_id)

    except Exception as e:
        flash(f"Erro ao carregar pets: {str(e)}", "error")
        return render_template("pets/listar.html", pets=[], pagination=None)

@pet_views_bp.route("/pets/novo", methods=["GET", "POST"])
def novo_pet():
    """Página de cadastro de novo pet"""
    if request.method == "GET":
        # Buscar clientes ativos para o dropdown
        clientes = [c for c in cliente_service.get_all_clientes() if c.ativo]
        especies = pet_service.get_especies_disponiveis()
        sexos = pet_service.get_sexos_disponiveis()
        
        # Cliente pré-selecionado se vier da URL
        cliente_id = request.args.get("cliente_id", type=int)
        
        return render_template("pets/novo.html", 
                             clientes=clientes, 
                             especies=especies, 
                             sexos=sexos,
                             cliente_selecionado=cliente_id)

    try:
        data = request.form

        # Converter data de nascimento se fornecida
        data_nascimento = None
        if data.get("data_nascimento"):
            try:
                data_nascimento = datetime.strptime(data.get("data_nascimento"), "%Y-%m-%d").date()
            except ValueError:
                flash("Formato de data inválido", "error")
                return redirect(url_for("pet_views.novo_pet"))

        # Converter peso se fornecido
        peso = None
        if data.get("peso"):
            try:
                peso = float(data.get("peso"))
            except ValueError:
                flash("Peso deve ser um número válido", "error")
                return redirect(url_for("pet_views.novo_pet"))

        # Criar novo pet
        pet = pet_service.create_pet(
            nome=data.get("nome").strip(),
            especie=data.get("especie"),
            cliente_id=int(data.get("cliente_id")),
            raca=data.get("raca", "").strip() if data.get("raca", "").strip() else None,
            cor=data.get("cor", "").strip() if data.get("cor", "").strip() else None,
            sexo=data.get("sexo") if data.get("sexo") else None,
            data_nascimento=data_nascimento,
            peso=peso,
            observacoes=data.get("observacoes", "").strip() if data.get("observacoes", "").strip() else None,
        )

        flash(f"Pet {pet.nome} cadastrado com sucesso!", "success")
        return redirect(url_for("pet_views.visualizar_pet", pet_id=pet.id))

    except Exception as e:
        flash(f"Erro ao cadastrar pet: {str(e)}", "error")
        return redirect(url_for("pet_views.novo_pet"))

@pet_views_bp.route("/pets/<int:pet_id>")
def visualizar_pet(pet_id):
    """Página de visualização de pet"""
    try:
        pet = pet_service.get_pet_by_id(pet_id)
        if not pet:
            flash("Pet não encontrado", "error")
            return redirect(url_for("pet_views.listar_pets"))
        return render_template("pets/visualizar.html", pet=pet)

    except Exception as e:
        flash(f"Erro ao carregar pet: {str(e)}", "error")
        return redirect(url_for("pet_views.listar_pets"))

@pet_views_bp.route("/pets/<int:pet_id>/editar", methods=["GET", "POST"])
def editar_pet(pet_id):
    """Página de edição de pet"""
    try:
        pet = pet_service.get_pet_by_id(pet_id)
        if not pet:
            flash("Pet não encontrado", "error")
            return redirect(url_for("pet_views.listar_pets"))

        if request.method == "GET":
            # Buscar dados para os dropdowns
            clientes = [c for c in cliente_service.get_all_clientes() if c.ativo]
            especies = pet_service.get_especies_disponiveis()
            sexos = pet_service.get_sexos_disponiveis()
            
            return render_template("pets/editar.html", 
                                 pet=pet, 
                                 clientes=clientes, 
                                 especies=especies, 
                                 sexos=sexos)

        # Processar formulário POST
        data = request.form

        # Converter data de nascimento se fornecida
        data_nascimento = None
        if data.get("data_nascimento"):
            try:
                data_nascimento = datetime.strptime(data.get("data_nascimento"), "%Y-%m-%d").date()
            except ValueError:
                flash("Formato de data inválido", "error")
                return render_template("pets/editar.html", pet=pet)

        # Converter peso se fornecido
        peso = None
        if data.get("peso"):
            try:
                peso = float(data.get("peso"))
            except ValueError:
                flash("Peso deve ser um número válido", "error")
                return render_template("pets/editar.html", pet=pet)

        # Atualizar dados do pet
        pet_atualizado = pet_service.update_pet(
            pet_id=pet.id,
            nome=data.get("nome").strip(),
            especie=data.get("especie"),
            cliente_id=int(data.get("cliente_id")),
            raca=data.get("raca", "").strip() if data.get("raca", "").strip() else None,
            cor=data.get("cor", "").strip() if data.get("cor", "").strip() else None,
            sexo=data.get("sexo") if data.get("sexo") else None,
            data_nascimento=data_nascimento,
            peso=peso,
            observacoes=data.get("observacoes", "").strip() if data.get("observacoes", "").strip() else None,
            ativo=("ativo" in data),
        )

        flash(f"Pet {pet_atualizado.nome} atualizado com sucesso!", "success")
        return redirect(url_for("pet_views.visualizar_pet", pet_id=pet.id))

    except Exception as e:
        flash(f"Erro ao atualizar pet: {str(e)}", "error")
        return render_template("pets/editar.html", pet=pet)

@pet_views_bp.route("/pets/<int:pet_id>/deletar", methods=["POST"])
def deletar_pet(pet_id):
    """Desativar pet (soft delete)"""
    try:
        pet = pet_service.get_pet_by_id(pet_id)
        if not pet:
            flash("Pet não encontrado", "error")
            return redirect(url_for("pet_views.listar_pets"))

        # Verificar se tem agendamentos ativos
        # TODO: Implementar verificação de agendamentos quando estiver pronto
        
        # Soft delete - apenas desativar
        pet_service.deactivate_pet(pet_id)
        flash(f"Pet {pet.nome} foi desativado", "warning")

        return redirect(url_for("pet_views.listar_pets"))

    except Exception as e:
        flash(f"Erro ao desativar pet: {str(e)}", "error")
        return redirect(url_for("pet_views.visualizar_pet", pet_id=pet_id))

@pet_views_bp.route("/pets/<int:pet_id>/ativar", methods=["POST"])
def ativar_pet(pet_id):
    """Reativar pet"""
    try:
        pet = pet_service.activate_pet(pet_id)
        if not pet:
            flash("Pet não encontrado", "error")
            return redirect(url_for("pet_views.listar_pets"))

        flash(f"Pet {pet.nome} foi reativado", "success")
        return redirect(url_for("pet_views.visualizar_pet", pet_id=pet_id))

    except Exception as e:
        flash(f"Erro ao reativar pet: {str(e)}", "error")
        return redirect(url_for("pet_views.visualizar_pet", pet_id=pet_id))

# Rotas auxiliares para busca e filtros
@pet_views_bp.route("/pets/buscar")
def buscar_pets():
    """API endpoint para busca de pets (para autocomplete, etc)"""
    try:
        query = request.args.get("q", "")
        limit = min(request.args.get("limit", 10, type=int), 50)
        cliente_id = request.args.get("cliente_id", type=int)

        if not query or len(query) < 2:
            return jsonify({"pets": []})

        # Buscar pets
        if cliente_id:
            pets = pet_service.get_active_pets_by_cliente_id(cliente_id)
        else:
            pets = [p for p in pet_service.get_all_pets() if p.ativo]

        # Filtrar por query
        pets_filtrados = [p for p in pets if query.lower() in p.nome.lower() or 
                         (p.raca and query.lower() in p.raca.lower())]

        return jsonify({
            "pets": [
                {
                    "id": pet.id,
                    "nome": pet.nome,
                    "especie": pet.especie,
                    "raca": pet.raca,
                    "dono": pet.dono.nome,
                }
                for pet in pets_filtrados[:limit]
            ]
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500