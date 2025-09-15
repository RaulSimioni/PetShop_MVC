from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.model.services.cliente_service import ClienteService
from sqlalchemy import or_
import math

cliente_views_bp = Blueprint("cliente_views", __name__)
cliente_service = ClienteService()

@cliente_views_bp.route("/clientes")
def listar_clientes():
    """Página de listagem de clientes"""
    page = request.args.get("page", 1, type=int)
    per_page = 10
    search = request.args.get("search", "", type=str)
    status = request.args.get("status", "", type=str)

    try:
        # A lógica de filtragem e paginação precisará ser movida para o service ou um novo método no service
        # Por enquanto, vamos simplificar para listar todos os clientes ativos
        clientes = cliente_service.get_all_clientes()

        # TODO: Implementar busca e paginação no ClienteService
        # Para fins de demonstração, vamos filtrar e paginar aqui temporariamente
        if search:
            clientes = [c for c in clientes if search.lower() in c.nome.lower() or search.lower() in c.cpf.lower() or (c.email and search.lower() in c.email.lower())]
        if status == 'true':
            clientes = [c for c in clientes if c.ativo]
        elif status == 'false':
            clientes = [c for c in clientes if not c.ativo]

        total_clientes = len(clientes)
        total_pages = math.ceil(total_clientes / per_page)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        clientes_paginados = clientes[start_index:end_index]

        # Criar um objeto de paginação simulado para o template
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

        pagination = Pagination(page, per_page, total_clientes, clientes_paginados)

        return render_template("clientes/listar.html", clientes=clientes_paginados, pagination=pagination, search=search, status=status)

    except Exception as e:
        flash(f"Erro ao carregar clientes: {str(e)}", "error")
        return render_template("clientes/listar.html", clientes=[], pagination=None)

@cliente_views_bp.route("/clientes/novo", methods=["GET", "POST"])
def novo_cliente():
    """Página de cadastro de novo cliente"""
    if request.method == "GET":
        return render_template("clientes/novo.html")

    try:
        data = request.form

        # Criar novo cliente
        cliente = cliente_service.create_cliente(
            nome=data.get("nome").strip(),
            cpf=data.get("cpf"),
            telefone=data.get("telefone"),
            email=data.get("email", "").strip() if data.get("email", "").strip() else None,
            endereco=data.get("endereco", "").strip() if data.get("endereco", "").strip() else None,
        )

        flash(f"Cliente {cliente.nome} cadastrado com sucesso!", "success")
        return redirect(url_for("cliente_views.visualizar_cliente", cliente_id=cliente.id))

    except Exception as e:
        flash(f"Erro ao cadastrar cliente: {str(e)}", "error")
        return render_template("clientes/novo.html")

@cliente_views_bp.route("/clientes/<int:cliente_id>")
def visualizar_cliente(cliente_id):
    """Página de visualização de cliente"""
    try:
        cliente = cliente_service.get_cliente_by_id(cliente_id)
        if not cliente:
            flash("Cliente não encontrado", "error")
            return redirect(url_for("cliente_views.listar_clientes"))
        return render_template("clientes/visualizar.html", cliente=cliente)

    except Exception as e:
        flash(f"Erro ao carregar cliente: {str(e)}", "error")
        return redirect(url_for("cliente_views.listar_clientes"))

@cliente_views_bp.route("/clientes/<int:cliente_id>/editar", methods=["GET", "POST"])
def editar_cliente(cliente_id):
    """Página de edição de cliente"""
    try:
        cliente = cliente_service.get_cliente_by_id(cliente_id)
        if not cliente:
            flash("Cliente não encontrado", "error")
            return redirect(url_for("cliente_views.listar_clientes"))

        if request.method == "GET":
            return render_template("clientes/editar.html", cliente=cliente)

        # Processar formulário POST
        data = request.form

        # Atualizar dados do cliente
        cliente_atualizado = cliente_service.update_cliente(
            cliente_id=cliente.id,
            nome=data.get("nome").strip(),
            cpf=data.get("cpf"),
            telefone=data.get("telefone"),
            email=data.get("email", "").strip() if data.get("email", "").strip() else None,
            endereco=data.get("endereco", "").strip() if data.get("endereco", "").strip() else None,
            ativo=("ativo" in data),
        )

        flash(f"Cliente {cliente_atualizado.nome} atualizado com sucesso!", "success")
        return redirect(url_for("cliente_views.visualizar_cliente", cliente_id=cliente.id))

    except Exception as e:
        flash(f"Erro ao atualizar cliente: {str(e)}", "error")
        return render_template("clientes/editar.html", cliente=cliente)

@cliente_views_bp.route("/clientes/<int:cliente_id>/deletar", methods=["POST"])
def deletar_cliente(cliente_id):
    """Desativar cliente (soft delete)"""
    try:
        cliente = cliente_service.get_cliente_by_id(cliente_id)
        if not cliente:
            flash("Cliente não encontrado", "error")
            return redirect(url_for("cliente_views.listar_clientes"))

        # Verificar se tem pets, vendas ou agendamentos ativos
        # TODO: Mover esta lógica para o ClienteService ou um serviço de validação
        if cliente.pets or cliente.vendas or cliente.agendamentos:
            # Soft delete - apenas desativar
            cliente_service.deactivate_cliente(cliente_id)
            flash(f"Cliente {cliente.nome} foi desativado", "warning")
        else:
            # Se não tem relacionamentos, permite delete real (opcional)
            cliente_service.deactivate_cliente(cliente_id)
            flash(f"Cliente {cliente.nome} foi desativado", "warning")

        return redirect(url_for("cliente_views.listar_clientes"))

    except Exception as e:
        flash(f"Erro ao desativar cliente: {str(e)}", "error")
        return redirect(url_for("cliente_views.visualizar_cliente", cliente_id=cliente_id))

@cliente_views_bp.route("/clientes/<int:cliente_id>/ativar", methods=["POST"])
def ativar_cliente(cliente_id):
    """Reativar cliente"""
    try:
        cliente = cliente_service.activate_cliente(cliente_id)
        if not cliente:
            flash("Cliente não encontrado", "error")
            return redirect(url_for("cliente_views.listar_clientes"))

        flash(f"Cliente {cliente.nome} foi reativado", "success")
        return redirect(url_for("cliente_views.visualizar_cliente", cliente_id=cliente_id))

    except Exception as e:
        flash(f"Erro ao reativar cliente: {str(e)}", "error")
        return redirect(url_for("cliente_views.visualizar_cliente", cliente_id=cliente_id))

# Rotas auxiliares para busca e filtros
@cliente_views_bp.route("/clientes/buscar")
def buscar_clientes():
    """API endpoint para busca de clientes (para autocomplete, etc)"""
    try:
        query = request.args.get("q", "")
        limit = min(request.args.get("limit", 10, type=int), 50)

        if not query or len(query) < 2:
            return {"clientes": []}

        # TODO: Mover esta lógica de busca para o ClienteService
        clientes = cliente_service.get_all_clientes()
        clientes_filtrados = [c for c in clientes if c.ativo and (query.lower() in c.nome.lower() or query.lower() in c.cpf.lower() or (c.email and query.lower() in c.email.lower()))]

        return {
            "clientes": [
                {
                    "id": cliente.id,
                    "nome": cliente.nome,
                    "cpf": cliente.cpf,
                    "telefone": cliente.telefone,
                    "email": cliente.email,
                }
                for cliente in clientes_filtrados[:limit]
            ]
        }

    except Exception as e:
        return {"erro": str(e)}, 500



