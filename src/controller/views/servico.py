from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.model.services.servico_service import ServicoService

servico_views_bp = Blueprint('servico_views', __name__)
servico_service = ServicoService()

@servico_views_bp.route('/servicos')
def listar():
    try:
        # Parâmetros de filtro e paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '', type=str)
        categoria = request.args.get('categoria', '', type=str)
        status = request.args.get('status', '', type=str)
        
        # Buscar todos os serviços
        servicos = servico_service.get_all_servicos()
        
        # Aplicar filtros
        if search:
            servicos = [s for s in servicos if search.lower() in s.nome.lower() or 
                       (s.descricao and search.lower() in s.descricao.lower())]
        
        if categoria:
            servicos = [s for s in servicos if s.categoria == categoria]
            
        if status == 'ativo':
            servicos = [s for s in servicos if s.ativo]
        elif status == 'inativo':
            servicos = [s for s in servicos if not s.ativo]
        
        # Paginação manual
        total = len(servicos)
        start = (page - 1) * per_page
        end = start + per_page
        servicos_paginados = servicos[start:end]
        
        # Calcular informações da paginação
        has_prev = page > 1
        has_next = end < total
        prev_num = page - 1 if has_prev else None
        next_num = page + 1 if has_next else None
        total_pages = (total + per_page - 1) // per_page
        
        # Obter categorias para o filtro
        categorias = servico_service.get_categorias_disponiveis()
        
        return render_template('servicos/listar.html',
                             servicos=servicos_paginados,
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
                             categoria_filtro=categoria,
                             status_filtro=status,
                             categorias=categorias)
    except Exception as e:
        flash(f'Erro ao carregar serviços: {str(e)}', 'danger')
        return render_template('servicos/listar.html', servicos=[], pagination={})

@servico_views_bp.route('/servicos/novo')
def novo():
    categorias = servico_service.get_categorias_disponiveis()
    return render_template('servicos/novo.html', categorias=categorias)

@servico_views_bp.route('/servicos/criar', methods=['POST'])
def criar():
    try:
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        preco = float(request.form.get('preco'))
        descricao = request.form.get('descricao')
        duracao_estimada = request.form.get('duracao_estimada')
        observacoes = request.form.get('observacoes')
        
        # Converter duração estimada para inteiro se fornecida
        if duracao_estimada:
            duracao_estimada = int(duracao_estimada)
        else:
            duracao_estimada = None
            
        servico = servico_service.create_servico(
            nome=nome,
            categoria=categoria,
            preco=preco,
            descricao=descricao,
            duracao_estimada=duracao_estimada,
            observacoes=observacoes
        )
        
        flash('Serviço criado com sucesso!', 'success')
        return redirect(url_for('servico_views.visualizar', id=servico.id))
        
    except ValueError as e:
        flash(str(e), 'danger')
        categorias = servico_service.get_categorias_disponiveis()
        return render_template('servicos/novo.html', categorias=categorias)
    except Exception as e:
        flash(f'Erro ao criar serviço: {str(e)}', 'danger')
        categorias = servico_service.get_categorias_disponiveis()
        return render_template('servicos/novo.html', categorias=categorias)

@servico_views_bp.route('/servicos/<int:id>')
def visualizar(id):
    try:
        servico = servico_service.get_servico_by_id(id)
        if not servico:
            flash('Serviço não encontrado', 'warning')
            return redirect(url_for('servico_views.listar'))
        
        # Obter estatísticas gerais
        estatisticas = servico_service.get_servicos_estatisticas()
        
        return render_template('servicos/visualizar.html', 
                             servico=servico,
                             estatisticas=estatisticas)
    except Exception as e:
        flash(f'Erro ao carregar serviço: {str(e)}', 'danger')
        return redirect(url_for('servico_views.listar'))

@servico_views_bp.route('/servicos/<int:id>/editar')
def editar(id):
    try:
        servico = servico_service.get_servico_by_id(id)
        if not servico:
            flash('Serviço não encontrado', 'warning')
            return redirect(url_for('servico_views.listar'))
        
        categorias = servico_service.get_categorias_disponiveis()
        estatisticas = servico_service.get_servicos_estatisticas()
        
        return render_template('servicos/editar.html', 
                             servico=servico,
                             categorias=categorias,
                             estatisticas=estatisticas)
    except Exception as e:
        flash(f'Erro ao carregar serviço: {str(e)}', 'danger')
        return redirect(url_for('servico_views.listar'))

@servico_views_bp.route('/servicos/<int:id>/atualizar', methods=['POST'])
def atualizar(id):
    try:
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        preco = float(request.form.get('preco'))
        descricao = request.form.get('descricao')
        duracao_estimada = request.form.get('duracao_estimada')
        observacoes = request.form.get('observacoes')
        ativo = request.form.get('ativo') == 'true'
        
        # Converter duração estimada para inteiro se fornecida
        if duracao_estimada:
            duracao_estimada = int(duracao_estimada)
        else:
            duracao_estimada = None
            
        servico = servico_service.update_servico(
            servico_id=id,
            nome=nome,
            categoria=categoria,
            preco=preco,
            descricao=descricao,
            duracao_estimada=duracao_estimada,
            observacoes=observacoes,
            ativo=ativo
        )
        
        flash('Serviço atualizado com sucesso!', 'success')
        return redirect(url_for('servico_views.visualizar', id=servico.id))
        
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('servico_views.editar', id=id))
    except Exception as e:
        flash(f'Erro ao atualizar serviço: {str(e)}', 'danger')
        return redirect(url_for('servico_views.editar', id=id))

@servico_views_bp.route('/servicos/<int:id>/toggle-status', methods=['POST'])
def toggle_status(id):
    try:
        servico = servico_service.get_servico_by_id(id)
        if not servico:
            return jsonify({'success': False, 'message': 'Serviço não encontrado'})
        
        if servico.ativo:
            servico_service.deactivate_servico(id)
            message = 'Serviço desativado com sucesso'
        else:
            servico_service.activate_servico(id)
            message = 'Serviço ativado com sucesso'
        
        return jsonify({'success': True, 'message': message, 'ativo': not servico.ativo})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro: {str(e)}'})

@servico_views_bp.route('/servicos/api/estatisticas')
def api_estatisticas():
    try:
        estatisticas = servico_service.get_servicos_estatisticas()
        return jsonify(estatisticas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500