from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.model.services.funcionario_service import FuncionarioService
from sqlalchemy import or_
import math

funcionario_views_bp = Blueprint("funcionario_views", __name__)
funcionario_service = FuncionarioService()

@funcionario_views_bp.route("/funcionarios")
def listar_funcionarios():
    """Página de listagem de funcionários"""
    page = request.args.get("page", 1, type=int)
    per_page = 10
    search = request.args.get("search", "", type=str)
    status = request.args.get("status", "", type=str)

    try:
        # A lógica de filtragem e paginação precisará ser movida para o service ou um novo método no service
        # Por enquanto, vamos simplificar para listar todos os funcionários ativos
        funcionarios = funcionario_service.get_all_funcionarios()

        # TODO: Implementar busca e paginação no FuncionarioService
        # Para fins de demonstração, vamos filtrar e paginar aqui temporariamente
        if search:
            funcionarios = [f for f in funcionarios if search.lower() in f.nome.lower() or search.lower() in f.cpf.lower() or (f.email and search.lower() in f.email.lower()) or search.lower() in f.cargo.lower()]
        if status == 'true':
            funcionarios = [f for f in funcionarios if f.ativo]
        elif status == 'false':
            funcionarios = [f for f in funcionarios if not f.ativo]

        total_funcionarios = len(funcionarios)
        total_pages = math.ceil(total_funcionarios / per_page)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        funcionarios_paginados = funcionarios[start_index:end_index]

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

        pagination = Pagination(page, per_page, total_funcionarios, funcionarios_paginados)

        return render_template("funcionarios/listar.html", funcionarios=funcionarios_paginados, pagination=pagination, search=search, status=status)

    except Exception as e:
        flash(f"Erro ao carregar funcionários: {str(e)}", "error")
        return render_template("funcionarios/listar.html", funcionarios=[], pagination=None)

@funcionario_views_bp.route("/funcionarios/novo", methods=["GET", "POST"])
def novo_funcionario():
    """Página de cadastro de novo funcionário"""
    if request.method == "GET":
        return render_template("funcionarios/novo.html")

    try:
        data = request.form

        # Criar novo funcionário
        funcionario = funcionario_service.create_funcionario(
            nome=data.get("nome").strip(),
            cpf=data.get("cpf"),
            telefone=data.get("telefone"),
            email=data.get("email", "").strip() if data.get("email", "").strip() else None,
            endereco=data.get("endereco", "").strip() if data.get("endereco", "").strip() else None,
            cargo=data.get("cargo").strip(),
            salario=float(data.get("salario")) if data.get("salario") else None,
            data_admissao=data.get("data_admissao")
        )

        flash(f"Funcionário {funcionario.nome} cadastrado com sucesso!", "success")
        return redirect(url_for("funcionario_views.visualizar_funcionario", funcionario_id=funcionario.id))

    except Exception as e:
        flash(f"Erro ao cadastrar funcionário: {str(e)}", "error")
        return render_template("funcionarios/novo.html")

@funcionario_views_bp.route("/funcionarios/<int:funcionario_id>")
def visualizar_funcionario(funcionario_id):
    """Página de visualização de funcionário"""
    try:
        funcionario = funcionario_service.get_funcionario_by_id(funcionario_id)
        if not funcionario:
            flash("Funcionário não encontrado", "error")
            return redirect(url_for("funcionario_views.listar_funcionarios"))
        return render_template("funcionarios/visualizar.html", funcionario=funcionario)

    except Exception as e:
        flash(f"Erro ao carregar funcionário: {str(e)}", "error")
        return redirect(url_for("funcionario_views.listar_funcionarios"))

@funcionario_views_bp.route("/funcionarios/<int:funcionario_id>/editar", methods=["GET", "POST"])
def editar_funcionario(funcionario_id):
    """Página de edição de funcionário"""
    try:
        funcionario = funcionario_service.get_funcionario_by_id(funcionario_id)
        if not funcionario:
            flash("Funcionário não encontrado", "error")
            return redirect(url_for("funcionario_views.listar_funcionarios"))

        if request.method == "GET":
            return render_template("funcionarios/editar.html", funcionario=funcionario)

        # Processar formulário POST
        data = request.form

        # Atualizar dados do funcionário
        funcionario_atualizado = funcionario_service.update_funcionario(
            funcionario_id=funcionario.id,
            nome=data.get("nome").strip(),
            cpf=data.get("cpf"),
            telefone=data.get("telefone"),
            email=data.get("email", "").strip() if data.get("email", "").strip() else None,
            endereco=data.get("endereco", "").strip() if data.get("endereco", "").strip() else None,
            cargo=data.get("cargo").strip(),
            salario=float(data.get("salario")) if data.get("salario") else None,
            data_admissao=data.get("data_admissao"),
            data_demissao=data.get("data_demissao") if data.get("data_demissao") else None,
            ativo=("ativo" in data),
        )

        flash(f"Funcionário {funcionario_atualizado.nome} atualizado com sucesso!", "success")
        return redirect(url_for("funcionario_views.visualizar_funcionario", funcionario_id=funcionario.id))

    except Exception as e:
        flash(f"Erro ao atualizar funcionário: {str(e)}", "error")
        return render_template("funcionarios/editar.html", funcionario=funcionario)

@funcionario_views_bp.route("/funcionarios/<int:funcionario_id>/deletar", methods=["POST"])
def deletar_funcionario(funcionario_id):
    """Desativar funcionário (soft delete)"""
    try:
        funcionario = funcionario_service.get_funcionario_by_id(funcionario_id)
        if not funcionario:
            flash("Funcionário não encontrado", "error")
            return redirect(url_for("funcionario_views.listar_funcionarios"))

        # Verificar se tem vendas ou agendamentos ativos
        # TODO: Mover esta lógica para o FuncionarioService ou um serviço de validação
        if funcionario.vendas or funcionario.agendamentos:
            # Soft delete - apenas desativar
            funcionario_service.deactivate_funcionario(funcionario_id)
            flash(f"Funcionário {funcionario.nome} foi desativado", "warning")
        else:
            # Se não tem relacionamentos, permite delete real (opcional)
            funcionario_service.deactivate_funcionario(funcionario_id)
            flash(f"Funcionário {funcionario.nome} foi desativado", "warning")

        return redirect(url_for("funcionario_views.listar_funcionarios"))

    except Exception as e:
        flash(f"Erro ao desativar funcionário: {str(e)}", "error")
        return redirect(url_for("funcionario_views.visualizar_funcionario", funcionario_id=funcionario_id))

@funcionario_views_bp.route("/funcionarios/<int:funcionario_id>/ativar", methods=["POST"])
def ativar_funcionario(funcionario_id):
    """Reativar funcionário"""
    try:
        funcionario = funcionario_service.activate_funcionario(funcionario_id)
        if not funcionario:
            flash("Funcionário não encontrado", "error")
            return redirect(url_for("funcionario_views.listar_funcionarios"))

        flash(f"Funcionário {funcionario.nome} foi reativado", "success")
        return redirect(url_for("funcionario_views.visualizar_funcionario", funcionario_id=funcionario_id))

    except Exception as e:
        flash(f"Erro ao reativar funcionário: {str(e)}", "error")
        return redirect(url_for("funcionario_views.visualizar_funcionario", funcionario_id=funcionario_id))

# Rotas auxiliares para busca e filtros
@funcionario_views_bp.route("/funcionarios/buscar")
def buscar_funcionarios():
    """API endpoint para busca de funcionários (para autocomplete, etc)"""
    try:
        query = request.args.get("q", "")
        limit = min(request.args.get("limit", 10, type=int), 50)

        if not query or len(query) < 2:
            return {"funcionarios": []}

        # TODO: Mover esta lógica de busca para o FuncionarioService
        funcionarios = funcionario_service.get_all_funcionarios()
        funcionarios_filtrados = [f for f in funcionarios if f.ativo and (query.lower() in f.nome.lower() or query.lower() in f.cpf.lower() or (f.email and query.lower() in f.email.lower()) or query.lower() in f.cargo.lower())]

        return {
            "funcionarios": [
                {
                    "id": funcionario.id,
                    "nome": funcionario.nome,
                    "cpf": funcionario.cpf,
                    "telefone": funcionario.telefone,
                    "email": funcionario.email,
                    "cargo": funcionario.cargo,
                }
                for funcionario in funcionarios_filtrados[:limit]
            ]
        }

    except Exception as e:
        return {"erro": str(e)}, 500