from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.model.services.agendamento_service import AgendamentoService
from src.model.services.cliente_service import ClienteService
from src.model.services.funcionario_service import FuncionarioService
from src.model.services.servico_service import ServicoService
from datetime import datetime, date

agendamento_views_bp = Blueprint('agendamento_views', __name__)
agendamento_service = AgendamentoService()
cliente_service = ClienteService()
funcionario_service = FuncionarioService()
servico_service = ServicoService()

@agendamento_views_bp.route('/agendamentos')
def listar():
    try:
        # Parâmetros de filtro e paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '', type=str)
        status = request.args.get('status', '', type=str)
        cliente_id = request.args.get('cliente_id', '', type=str)
        funcionario_id = request.args.get('funcionario_id', '', type=str)
        data_inicio = request.args.get('data_inicio', '', type=str)
        data_fim = request.args.get('data_fim', '', type=str)
        
        # Buscar todos os agendamentos
        agendamentos = agendamento_service.get_all_agendamentos()
        
        # Aplicar filtros
        if search:
            agendamentos = [a for a in agendamentos if 
                           (a.cliente and search.lower() in a.cliente.nome.lower()) or
                           (a.servico and search.lower() in a.servico.nome.lower()) or
                           (a.funcionario and search.lower() in a.funcionario.nome.lower()) or
                           (a.observacoes and search.lower() in a.observacoes.lower())]
        
        if status:
            agendamentos = [a for a in agendamentos if a.status == status]
            
        if cliente_id:
            agendamentos = [a for a in agendamentos if str(a.cliente_id) == cliente_id]
            
        if funcionario_id:
            agendamentos = [a for a in agendamentos if str(a.funcionario_id) == funcionario_id]
        
        # Filtro por data
        if data_inicio:
            data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
            agendamentos = [a for a in agendamentos if a.data_agendamento >= data_inicio_dt]
            
        if data_fim:
            data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
            agendamentos = [a for a in agendamentos if a.data_agendamento <= data_fim_dt]
        
        # Ordenar por data de agendamento
        agendamentos.sort(key=lambda x: x.data_agendamento, reverse=True)
        
        # Paginação manual
        total = len(agendamentos)
        start = (page - 1) * per_page
        end = start + per_page
        agendamentos_paginados = agendamentos[start:end]
        
        # Calcular informações da paginação
        has_prev = page > 1
        has_next = end < total
        prev_num = page - 1 if has_prev else None
        next_num = page + 1 if has_next else None
        total_pages = (total + per_page - 1) // per_page
        
        # Obter dados para filtros
        clientes = cliente_service.get_all_clientes()
        funcionarios = funcionario_service.get_all_funcionarios()
        status_disponiveis = agendamento_service.get_status_disponiveis()
        
        return render_template('agendamentos/listar.html',
                             agendamentos=agendamentos_paginados,
                             pagination={
                                 'page': page,
                                 'per_page': per_page,
                                 'total': total,
                                 'has_prev': has_prev,
                                 'has_next': has_next,
                                 'prev_num': prev_num,
                                 'next_num': next_num,
                                 'pages': total_pages
                             },
                             search=search,
                             status_filtro=status,
                             cliente_filtro=cliente_id,
                             funcionario_filtro=funcionario_id,
                             data_inicio_filtro=data_inicio,
                             data_fim_filtro=data_fim,
                             clientes=clientes,
                             funcionarios=funcionarios,
                             status_disponiveis=status_disponiveis)
    except Exception as e:
        flash(f'Erro ao carregar agendamentos: {str(e)}', 'danger')
        return render_template('agendamentos/listar.html', agendamentos=[], pagination={})

@agendamento_views_bp.route('/agendamentos/novo')
def novo():
    clientes = cliente_service.get_all_clientes()
    funcionarios = funcionario_service.get_all_funcionarios()
    servicos = servico_service.get_all_servicos()
    return render_template('agendamentos/novo.html', 
                         clientes=clientes, 
                         funcionarios=funcionarios, 
                         servicos=servicos)

@agendamento_views_bp.route('/agendamentos/criar', methods=['POST'])
def criar():
    try:
        cliente_id = int(request.form.get('cliente_id'))
        servico_id = int(request.form.get('servico_id'))
        data_agendamento_str = request.form.get('data_agendamento')
        funcionario_id = request.form.get('funcionario_id')
        observacoes = request.form.get('observacoes')
        valor_estimado = request.form.get('valor_estimado')
        
        # Converter funcionario_id para int se fornecido
        if funcionario_id:
            funcionario_id = int(funcionario_id)
        else:
            funcionario_id = None
            
        # Converter valor_estimado para float se fornecido
        if valor_estimado:
            valor_estimado = float(valor_estimado)
        else:
            valor_estimado = None
            
        # Converter data_agendamento para datetime
        data_agendamento = datetime.fromisoformat(data_agendamento_str)
            
        agendamento = agendamento_service.create_agendamento(
            cliente_id=cliente_id,
            servico_id=servico_id,
            data_agendamento=data_agendamento,
            funcionario_id=funcionario_id,
            pet_id=None,  # Por enquanto None até pets ser implementado
            observacoes=observacoes,
            valor_estimado=valor_estimado
        )
        
        flash('Agendamento criado com sucesso!', 'success')
        return redirect(url_for('agendamento_views.visualizar', id=agendamento.id))
        
    except ValueError as e:
        flash(str(e), 'danger')
        clientes = cliente_service.get_all_clientes()
        funcionarios = funcionario_service.get_all_funcionarios()
        servicos = servico_service.get_all_servicos()
        return render_template('agendamentos/novo.html', 
                             clientes=clientes, 
                             funcionarios=funcionarios, 
                             servicos=servicos)
    except Exception as e:
        flash(f'Erro ao criar agendamento: {str(e)}', 'danger')
        clientes = cliente_service.get_all_clientes()
        funcionarios = funcionario_service.get_all_funcionarios()
        servicos = servico_service.get_all_servicos()
        return render_template('agendamentos/novo.html', 
                             clientes=clientes, 
                             funcionarios=funcionarios, 
                             servicos=servicos)

@agendamento_views_bp.route('/agendamentos/<int:id>')
def visualizar(id):
    try:
        agendamento = agendamento_service.get_agendamento_by_id(id)
        if not agendamento:
            flash('Agendamento não encontrado', 'warning')
            return redirect(url_for('agendamento_views.listar'))
        
        # Obter estatísticas gerais
        estatisticas = agendamento_service.get_agendamentos_estatisticas()
        
        return render_template('agendamentos/visualizar.html', 
                             agendamento=agendamento,
                             estatisticas=estatisticas)
    except Exception as e:
        flash(f'Erro ao carregar agendamento: {str(e)}', 'danger')
        return redirect(url_for('agendamento_views.listar'))

@agendamento_views_bp.route('/agendamentos/<int:id>/editar')
def editar(id):
    try:
        agendamento = agendamento_service.get_agendamento_by_id(id)
        if not agendamento:
            flash('Agendamento não encontrado', 'warning')
            return redirect(url_for('agendamento_views.listar'))
        
        clientes = cliente_service.get_all_clientes()
        funcionarios = funcionario_service.get_all_funcionarios()
        servicos = servico_service.get_all_servicos()
        status_disponiveis = agendamento_service.get_status_disponiveis()
        estatisticas = agendamento_service.get_agendamentos_estatisticas()
        
        return render_template('agendamentos/editar.html', 
                             agendamento=agendamento,
                             clientes=clientes,
                             funcionarios=funcionarios,
                             servicos=servicos,
                             status_disponiveis=status_disponiveis,
                             estatisticas=estatisticas)
    except Exception as e:
        flash(f'Erro ao carregar agendamento: {str(e)}', 'danger')
        return redirect(url_for('agendamento_views.listar'))

@agendamento_views_bp.route('/agendamentos/<int:id>/atualizar', methods=['POST'])
def atualizar(id):
    try:
        cliente_id = int(request.form.get('cliente_id'))
        servico_id = int(request.form.get('servico_id'))
        data_agendamento_str = request.form.get('data_agendamento')
        funcionario_id = request.form.get('funcionario_id')
        status = request.form.get('status')
        observacoes = request.form.get('observacoes')
        valor_estimado = request.form.get('valor_estimado')
        
        # Converter funcionario_id para int se fornecido
        if funcionario_id:
            funcionario_id = int(funcionario_id)
        else:
            funcionario_id = None
            
        # Converter valor_estimado para float se fornecido
        if valor_estimado:
            valor_estimado = float(valor_estimado)
        else:
            valor_estimado = None
            
        # Converter data_agendamento para datetime
        data_agendamento = datetime.fromisoformat(data_agendamento_str)
            
        agendamento = agendamento_service.update_agendamento(
            agendamento_id=id,
            cliente_id=cliente_id,
            servico_id=servico_id,
            data_agendamento=data_agendamento,
            funcionario_id=funcionario_id,
            status=status,
            observacoes=observacoes,
            valor_estimado=valor_estimado
        )
        
        flash('Agendamento atualizado com sucesso!', 'success')
        return redirect(url_for('agendamento_views.visualizar', id=agendamento.id))
        
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('agendamento_views.editar', id=id))
    except Exception as e:
        flash(f'Erro ao atualizar agendamento: {str(e)}', 'danger')
        return redirect(url_for('agendamento_views.editar', id=id))

@agendamento_views_bp.route('/agendamentos/<int:id>/status', methods=['POST'])
def update_status(id):
    try:
        data = request.get_json()
        status = data.get('status')
        
        agendamento = agendamento_service.update_status(id, status)
        
        return jsonify({
            'success': True, 
            'message': f'Status atualizado para {status}',
            'status': agendamento.status
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro: {str(e)}'})

@agendamento_views_bp.route('/agendamentos/<int:id>/cancelar', methods=['POST'])
def cancelar(id):
    try:
        agendamento = agendamento_service.cancel_agendamento(id)
        return jsonify({
            'success': True, 
            'message': 'Agendamento cancelado com sucesso',
            'status': agendamento.status
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro: {str(e)}'})

@agendamento_views_bp.route('/agendamentos/<int:id>/confirmar', methods=['POST'])
def confirmar(id):
    try:
        agendamento = agendamento_service.confirm_agendamento(id)
        return jsonify({
            'success': True, 
            'message': 'Agendamento confirmado com sucesso',
            'status': agendamento.status
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro: {str(e)}'})

@agendamento_views_bp.route('/agendamentos/api/estatisticas')
def api_estatisticas():
    try:
        estatisticas = agendamento_service.get_agendamentos_estatisticas()
        return jsonify(estatisticas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500